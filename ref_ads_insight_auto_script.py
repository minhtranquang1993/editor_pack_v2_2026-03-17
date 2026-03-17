#!/usr/bin/env python3
"""
ads_insight.py — Phân tích sâu EOD ads, gửi 1 tin Telegram lúc 19h ICT.

Dùng cho OpenClaw skill: ads-insight-auto
Cron: 0 12 * * * (12h UTC = 19h ICT)

Workflow:
  1. Query Supabase daily_ads_report (hôm nay + 7 ngày trước)
  2. Tính baseline 7-day avg per platform
  3. Apply insight rules (CPL spike, CTR drop, spend alert, zero leads)
  4. Build Telegram message
  5. Gửi 1 tin/ngày, lưu insight vào memory/insights/

Dependencies: supabase, requests, pandas
Credentials:
  - credentials/report_ads_secrets.json  → sb_url, sb_key (report Supabase)
  - credentials/telegram_token.txt
"""

import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent          # skills/ads-insight-auto/
WORKSPACE_DIR = BASE_DIR.parent.parent                      # repo root
CRED_DIR = WORKSPACE_DIR / "credentials"
MEMORY_DIR = WORKSPACE_DIR / "memory" / "insights"
SECRETS_PATH = CRED_DIR / "report_ads_secrets.json"
TELEGRAM_TOKEN_PATH = CRED_DIR / "telegram_token.txt"

# ── Import Hands Framework ───────────────────────────────────────────────────
sys.path.insert(0, str(WORKSPACE_DIR / "skills" / "hands-framework" / "scripts"))
from hands_core import HandState, HandLogger, send_telegram, run_hand

HAND_NAME = "ads-insight-auto"
ICT = timezone(timedelta(hours=7))

# ── Constants ────────────────────────────────────────────────────────────────
PLATFORMS = ["fb", "tiktok", "google"]
CPL_SPIKE_THRESHOLD = 1.20    # +20%
CPL_DROP_THRESHOLD = 0.85     # -15%
CTR_DROP_THRESHOLD = 0.85     # -15%
SPEND_OVER_THRESHOLD = 1.20   # +20% vs avg


# ── Credentials ──────────────────────────────────────────────────────────────
def load_secrets() -> dict:
    if not SECRETS_PATH.exists():
        raise FileNotFoundError(f"Missing: {SECRETS_PATH}")
    return json.loads(SECRETS_PATH.read_text())


def load_telegram_token() -> str:
    if not TELEGRAM_TOKEN_PATH.exists():
        raise FileNotFoundError(f"Missing: {TELEGRAM_TOKEN_PATH}")
    return TELEGRAM_TOKEN_PATH.read_text().strip()


# ── Supabase Query ────────────────────────────────────────────────────────────
def fetch_report_data(sb_url: str, sb_key: str, days: int = 8) -> list[dict]:
    """Fetch daily_ads_report cho N ngày gần nhất."""
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    url = f"{sb_url}/rest/v1/daily_ads_report"
    headers = {
        "apikey": sb_key,
        "Authorization": f"Bearer {sb_key}",
        "Content-Type": "application/json",
    }
    params = {
        "select": "report_date,platform,branch,cost,impressions,clicks,cpm,cpc,leads",
        "report_date": f"gte.{cutoff}",
        "order": "report_date.desc",
    }
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


# ── Aggregation ───────────────────────────────────────────────────────────────
def aggregate_by_platform(rows: list[dict]) -> dict:
    """
    Group rows by (platform, report_date), sum cost/impressions/clicks/leads.
    Returns: { platform: { date_str: {cost, impressions, clicks, leads, ctr, cpl} } }
    """
    agg = {}
    for row in rows:
        plat = (row.get("platform") or "").lower()
        d = row.get("report_date", "")
        if not plat or not d:
            continue
        if plat not in agg:
            agg[plat] = {}
        if d not in agg[plat]:
            agg[plat][d] = {"cost": 0, "impressions": 0, "clicks": 0, "leads": 0}
        agg[plat][d]["cost"] += float(row.get("cost") or 0)
        agg[plat][d]["impressions"] += int(row.get("impressions") or 0)
        agg[plat][d]["clicks"] += int(row.get("clicks") or 0)
        agg[plat][d]["leads"] += int(row.get("leads") or 0)

    # Tính CTR, CPL
    for plat in agg:
        for d in agg[plat]:
            e = agg[plat][d]
            e["ctr"] = (e["clicks"] / e["impressions"] * 100) if e["impressions"] > 0 else 0
            e["cpl"] = (e["cost"] / e["leads"]) if e["leads"] > 0 else 0

    return agg


def calc_baseline(agg: dict, today_str: str) -> dict:
    """
    Tính avg 7 ngày trước (không gồm hôm nay) cho mỗi platform.
    Returns: { platform: {avg_cost, avg_cpl, avg_ctr, avg_cpc} }
    """
    baseline = {}
    for plat, dates in agg.items():
        hist = {d: v for d, v in dates.items() if d < today_str}
        if not hist:
            baseline[plat] = {}
            continue
        costs = [v["cost"] for v in hist.values()]
        cpls = [v["cpl"] for v in hist.values() if v["cpl"] > 0]
        ctrs = [v["ctr"] for v in hist.values()]
        baseline[plat] = {
            "avg_cost": sum(costs) / len(costs) if costs else 0,
            "avg_cpl": sum(cpls) / len(cpls) if cpls else 0,
            "avg_ctr": sum(ctrs) / len(ctrs) if ctrs else 0,
            "days": len(hist),
        }
    return baseline


# ── Insight Rules ─────────────────────────────────────────────────────────────
def apply_rules(today_data: dict, baseline: dict) -> tuple[list, list, list]:
    """
    Apply insight rules. Returns (alerts, summaries, actions).
    alerts = critical/warning lines
    summaries = per-platform summary lines
    actions = concrete next actions by platform
    """
    alerts = []
    summaries = []
    actions = []
    now_ict = datetime.now(ICT)

    for plat in ["fb", "tiktok", "google"]:
        t = today_data.get(plat, {})
        b = baseline.get(plat, {})

        cost = float(t.get("cost", 0) or 0)
        leads = int(t.get("leads", 0) or 0)
        cpl = float(t.get("cpl", 0) or 0)
        ctr = float(t.get("ctr", 0) or 0)
        avg_cpl = float(b.get("avg_cpl", 0) or 0)
        avg_ctr = float(b.get("avg_ctr", 0) or 0)
        avg_cost = float(b.get("avg_cost", 0) or 0)

        name = {"fb": "FB", "tiktok": "TikTok", "google": "Google"}[plat]

        # Summary line: xử lý rõ các case zero-delivery vs zero-lead-with-spend
        if leads == 0 and cost == 0:
            cpl_str = "N/A"
            trend = "⚪ no delivery"
        elif leads == 0 and cost > 0:
            cpl_str = "∞"
            trend = "🔴 zero lead"
        else:
            cpl_str = f"{cpl/1000:.0f}K"
            if avg_cpl > 0:
                pct = (cpl - avg_cpl) / avg_cpl * 100
                trend = f"↑{pct:.0f}%" if pct > 0 else f"↓{abs(pct):.0f}%"
            else:
                trend = "→ baseline thiếu"

        summaries.append(
            f"• {name}: Spend {cost/1_000_000:.1f}M | Lead {leads} | CPL {cpl_str} ({trend} vs avg)"
        )

        # Rule 1: zero lead sau 12h — tách rõ 2 trạng thái
        if leads == 0 and now_ict.hour >= 12:
            if cost > 0:
                alerts.append(f"🔴 CRITICAL: {name} lead = 0 sau {now_ict.hour}h dù đã spend {cost:,.0f}đ")
                actions.append(f"{name}: kiểm tra tracking + form/LP ngay; nếu thêm 1 ngày vẫn 0 lead thì pause adset yếu")
            else:
                alerts.append(f"⚠️ {name} spend = 0, lead = 0 → no delivery")
                actions.append(f"{name}: kiểm tra campaign status, budget, bid, lịch chạy và policy")

        # Rule 2: CPL spike
        if avg_cpl > 0 and leads > 0 and cpl > avg_cpl * CPL_SPIKE_THRESHOLD:
            pct = (cpl - avg_cpl) / avg_cpl * 100
            alerts.append(f"⚠️ {name} CPL spike +{pct:.0f}% vs avg → creative fatigue?")
            actions.append(f"{name}: giữ budget hiện tại, test 1-2 creative mới và rà audience")

        # Rule 3: CPL drop (tốt)
        if avg_cpl > 0 and leads > 0 and cpl < avg_cpl * CPL_DROP_THRESHOLD:
            pct = (avg_cpl - cpl) / avg_cpl * 100
            alerts.append(f"✅ {name} CPL cải thiện -{pct:.0f}% → cân nhắc scale budget +20%")
            actions.append(f"{name}: có thể scale +20% ngân sách nếu tần suất và CR vẫn ổn")

        # Rule 4: CTR drop
        if avg_ctr > 0 and ctr > 0 and ctr < avg_ctr * CTR_DROP_THRESHOLD:
            pct = (avg_ctr - ctr) / avg_ctr * 100
            alerts.append(f"🔥 {name} CTR giảm -{pct:.0f}% → creative fatigue, cần thay mẫu")
            actions.append(f"{name}: thay creative có CTR thấp, ưu tiên mẫu mới trong 24h")

        # Rule 5: Overspend vs avg
        if avg_cost > 0 and cost > avg_cost * SPEND_OVER_THRESHOLD:
            pct = (cost - avg_cost) / avg_cost * 100
            alerts.append(f"🚨 {name} spend vượt avg +{pct:.0f}% → check budget cap")
            actions.append(f"{name}: rà lại phân bổ budget theo adset, tránh over-spend một cụm")

    # Deduplicate actions (giữ thứ tự)
    uniq_actions = []
    seen = set()
    for a in actions:
        if a not in seen:
            uniq_actions.append(a)
            seen.add(a)

    return alerts, summaries, uniq_actions


# ── Build Message ─────────────────────────────────────────────────────────────
def build_message(today_str: str, summaries: list, alerts: list, actions: list) -> str:
    lines = [f"📊 *ADS INSIGHT — {today_str}*\n"]
    lines.append("*[SUMMARY]*")
    lines.extend(summaries)

    if alerts:
        lines.append("\n*[ALERTS]*")
        lines.extend(alerts)
    else:
        lines.append("\n✅ Không có anomaly — all platforms on track")

    if actions:
        lines.append("\n*[NEXT ACTIONS]*")
        for i, action in enumerate(actions[:4], 1):
            lines.append(f"{i}. {action}")

    lines.append(f"\n_Generated {datetime.now(ICT).strftime('%H:%M ICT')}_")
    return "\n".join(lines)


# ── Save Insight ──────────────────────────────────────────────────────────────
def save_insight(today_str: str, message: str):
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    path = MEMORY_DIR / f"{today_str}-ads.md"
    path.write_text(f"# Ads Insight {today_str}\n\n{message}\n")


# ── Main ──────────────────────────────────────────────────────────────────────
def main(state: HandState, logger: HandLogger):
    secrets = load_secrets()
    sb_url = secrets["report_sb_url"]
    sb_key = secrets["report_sb_key"]
    token = load_telegram_token()

    today_str = date.today().isoformat()

    logger.info("Fetching report data from Supabase...")
    rows = fetch_report_data(sb_url, sb_key, days=8)
    if not rows:
        logger.info("No data found — skip")
        return

    agg = aggregate_by_platform(rows)
    baseline = calc_baseline(agg, today_str)

    # Today data per platform
    today_data = {plat: agg.get(plat, {}).get(today_str, {}) for plat in ["fb", "tiktok", "google"]}

    alerts, summaries, actions = apply_rules(today_data, baseline)

    message = build_message(today_str, summaries, alerts, actions)

    logger.info("Sending Telegram insight...")
    send_telegram(message)

    save_insight(today_str, message)
    logger.info("Done.")


if __name__ == "__main__":
    # Load Hands Framework state & logger
    state = HandState.load(HAND_NAME)
    logger = HandLogger(HAND_NAME)
    
    # Define steps list — wrapper để pass state & logger vào main()
    steps = [
        {
            "name": "run_main",
            "fn": lambda: main(state, logger),
            "skip_if_done": False
        }
    ]
    
    # Run with hands framework
    run_hand(HAND_NAME, steps, state, logger)
