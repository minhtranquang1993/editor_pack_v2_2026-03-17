#!/usr/bin/env python3
"""
weekly_review.py — Tổng kết performance ads theo tuần hoặc tháng.

Dùng cho OpenClaw skill: weekly-review-auto
Cron weekly:  0 1 * * 1  (Thứ 2 8h ICT)
Cron monthly: 0 1 1 * *  (Ngày 1 8h ICT)

Usage:
  python3 weekly_review.py               # weekly (default)
  python3 weekly_review.py --mode monthly

Workflow:
  1. Query Supabase daily_ads_report kỳ hiện tại + kỳ trước
  2. Aggregate: cost, leads, CPL, CTR per platform
  3. So sánh % change vs kỳ trước
  4. Top 3 / Bottom 3 per platform (by CPL)
  5. Creative alerts: CTR giảm 3+ ngày liên tiếp
  6. Build report Telegram theo template references/report-template.md
  7. Gửi Telegram

Dependencies: supabase, requests, pandas
Credentials:
  - credentials/report_ads_secrets.json  → report_sb_url, report_sb_key
  - credentials/telegram_token.txt
"""

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import requests

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent      # skills/weekly-review-auto/
WORKSPACE_DIR = BASE_DIR.parent.parent                  # repo root
CRED_DIR = WORKSPACE_DIR / "credentials"
SECRETS_PATH = CRED_DIR / "report_ads_secrets.json"
TELEGRAM_TOKEN_PATH = CRED_DIR / "telegram_token.txt"

# ── Import Hands Framework ───────────────────────────────────────────────────
sys.path.insert(0, str(WORKSPACE_DIR / "skills" / "hands-framework" / "scripts"))
from hands_core import HandState, HandLogger, send_telegram, run_hand

HAND_NAME = "weekly-review-auto"
ICT = timezone(timedelta(hours=7))
PLATFORMS = ["fb", "tiktok", "google"]
PLAT_NAMES = {"fb": "Facebook", "tiktok": "TikTok", "google": "Google"}


# ── Credentials ──────────────────────────────────────────────────────────────
def load_secrets() -> dict:
    if not SECRETS_PATH.exists():
        raise FileNotFoundError(f"Missing: {SECRETS_PATH}")
    return json.loads(SECRETS_PATH.read_text())


def load_telegram_token() -> str:
    if not TELEGRAM_TOKEN_PATH.exists():
        raise FileNotFoundError(f"Missing: {TELEGRAM_TOKEN_PATH}")
    return TELEGRAM_TOKEN_PATH.read_text().strip()


# ── Date Ranges ───────────────────────────────────────────────────────────────
def get_weekly_ranges() -> tuple[tuple[date, date], tuple[date, date]]:
    """Current week (last 7 days) vs previous 7 days."""
    today = date.today()
    cur_end = today - timedelta(days=1)
    cur_start = today - timedelta(days=7)
    prev_end = cur_start - timedelta(days=1)
    prev_start = today - timedelta(days=14)
    return (cur_start, cur_end), (prev_start, prev_end)


def get_monthly_ranges() -> tuple[tuple[date, date], tuple[date, date]]:
    """Current month vs previous month."""
    today = date.today()
    cur_start = today.replace(day=1)
    cur_end = today - timedelta(days=1)

    prev_end = cur_start - timedelta(days=1)
    prev_start = prev_end.replace(day=1)
    return (cur_start, cur_end), (prev_start, prev_end)


# ── Supabase Query ────────────────────────────────────────────────────────────
def fetch_range(sb_url: str, sb_key: str, start: date, end: date) -> list[dict]:
    url = f"{sb_url}/rest/v1/daily_ads_report"
    headers = {"apikey": sb_key, "Authorization": f"Bearer {sb_key}"}
    params = {
        "select": "report_date,platform,branch,cost,impressions,clicks,cpm,cpc,leads",
        "report_date": f"gte.{start.isoformat()}",
        "and": f"(report_date.lte.{end.isoformat()})",
        "order": "report_date.asc",
    }
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    resp.raise_for_status()
    return resp.json()


# ── Aggregate ────────────────────────────────────────────────────────────────
def aggregate(rows: list[dict]) -> dict:
    """
    Returns { platform: {cost, leads, impressions, clicks, cpl, ctr, daily: {date: row}} }
    """
    agg = {}
    for row in rows:
        plat = (row.get("platform") or "").lower()
        if not plat:
            continue
        if plat not in agg:
            agg[plat] = {"cost": 0, "leads": 0, "impressions": 0, "clicks": 0, "daily": {}}
        d = row.get("report_date", "")
        agg[plat]["cost"] += float(row.get("cost") or 0)
        agg[plat]["leads"] += int(row.get("leads") or 0)
        agg[plat]["impressions"] += int(row.get("impressions") or 0)
        agg[plat]["clicks"] += int(row.get("clicks") or 0)
        if d:
            if d not in agg[plat]["daily"]:
                agg[plat]["daily"][d] = {"cost": 0, "impressions": 0, "clicks": 0, "leads": 0}
            agg[plat]["daily"][d]["cost"] += float(row.get("cost") or 0)
            agg[plat]["daily"][d]["impressions"] += int(row.get("impressions") or 0)
            agg[plat]["daily"][d]["clicks"] += int(row.get("clicks") or 0)
            agg[plat]["daily"][d]["leads"] += int(row.get("leads") or 0)

    for plat in agg:
        e = agg[plat]
        e["cpl"] = e["cost"] / e["leads"] if e["leads"] > 0 else 0
        e["ctr"] = e["clicks"] / e["impressions"] * 100 if e["impressions"] > 0 else 0
    return agg


def pct_change(cur: float, prev: float) -> str:
    if prev == 0:
        return "N/A"
    p = (cur - prev) / prev * 100
    return f"+{p:.0f}%↑" if p >= 0 else f"{p:.0f}%↓"


def fmt_cost(v: float) -> str:
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    return f"{v/1000:.0f}K"


# ── Creative Alert: CTR drop 3+ ngày liên tiếp ───────────────────────────────
def detect_creative_fatigue(cur_agg: dict) -> list[str]:
    alerts = []
    for plat, data in cur_agg.items():
        daily = data.get("daily", {})
        if len(daily) < 3:
            continue
        sorted_dates = sorted(daily.keys())
        ctrs = []
        for d in sorted_dates:
            row = daily[d]
            ctr = row["clicks"] / row["impressions"] * 100 if row["impressions"] > 0 else 0
            ctrs.append(ctr)
        # Check consecutive drops ≥ 3
        streak = 1
        for i in range(1, len(ctrs)):
            if ctrs[i] < ctrs[i - 1]:
                streak += 1
                if streak >= 3:
                    alerts.append(f"🔥 {PLAT_NAMES.get(plat, plat)}: CTR giảm {streak} ngày liên tiếp ({ctrs[-1]:.2f}%) → cân nhắc thay creative")
                    break
            else:
                streak = 1
    return alerts


# ── Build Report ──────────────────────────────────────────────────────────────
def build_report(mode: str, cur_range: tuple, prev_range: tuple,
                 cur_agg: dict, prev_agg: dict, creative_alerts: list) -> str:
    now_ict = datetime.now(ICT)
    if mode == "weekly":
        header = f"📊 *Weekly Review — {cur_range[0]} → {cur_range[1]}*"
    else:
        header = f"📊 *Monthly Review — {cur_range[0].strftime('%m/%Y')}*"

    lines = [header, f"📅 Generated: {now_ict.strftime('%d/%m/%Y %H:%M ICT')}\n"]

    # 1. Cost table
    lines.append("*1️⃣ CHI PHÍ*")
    total_cur = total_prev = 0
    for plat in PLATFORMS:
        cur = cur_agg.get(plat, {})
        prev = prev_agg.get(plat, {})
        c, p = cur.get("cost", 0), prev.get("cost", 0)
        total_cur += c
        total_prev += p
        lines.append(f"• {PLAT_NAMES[plat]}: {fmt_cost(c)} (vs {fmt_cost(p)} {pct_change(c, p)})")
    lines.append(f"• *TOTAL: {fmt_cost(total_cur)}* (vs {fmt_cost(total_prev)} {pct_change(total_cur, total_prev)})\n")

    # 2. Leads & CPL
    lines.append("*2️⃣ LEADS & CPL*")
    total_leads_cur = total_leads_prev = 0
    for plat in PLATFORMS:
        cur = cur_agg.get(plat, {})
        prev = prev_agg.get(plat, {})
        l_c, l_p = cur.get("leads", 0), prev.get("leads", 0)
        cpl_c, cpl_p = cur.get("cpl", 0), prev.get("cpl", 0)
        total_leads_cur += l_c
        total_leads_prev += l_p
        cpl_str = f"{cpl_c/1000:.0f}K" if cpl_c > 0 else "N/A"
        lines.append(f"• {PLAT_NAMES[plat]}: {l_c} leads | CPL {cpl_str} ({pct_change(cpl_c, cpl_p)})")
    lines.append(f"• *TOTAL: {total_leads_cur} leads* (vs {total_leads_prev})\n")

    # 3. Platform ranking (best CPL)
    ranked = sorted(
        [(p, cur_agg[p]) for p in PLATFORMS if p in cur_agg and cur_agg[p].get("cpl", 0) > 0],
        key=lambda x: x[1]["cpl"]
    )
    if ranked:
        lines.append("*3️⃣ PLATFORM RANKING (CPL thấp = hiệu quả cao)*")
        medals = ["🥇", "🥈", "🥉"]
        for i, (plat, data) in enumerate(ranked):
            m = medals[i] if i < 3 else "  "
            lines.append(f"{m} {PLAT_NAMES[plat]}: CPL {data['cpl']/1000:.0f}K | {data['leads']} leads")
        lines.append("")

    # 4. Creative alerts
    if creative_alerts:
        lines.append("*4️⃣ CREATIVE ALERTS*")
        lines.extend(creative_alerts)
        lines.append("")

    # 5. Recommendations
    lines.append("*5️⃣ KHUYẾN NGHỊ*")
    if ranked:
        best_plat = ranked[0][0]
        lines.append(f"✅ Scale {PLAT_NAMES[best_plat]} (CPL tốt nhất) +20% budget")
    if ranked and len(ranked) > 1:
        worst_plat = ranked[-1][0]
        worst_cpl = ranked[-1][1]["cpl"]
        best_cpl = ranked[0][1]["cpl"]
        if worst_cpl > best_cpl * 1.5:
            lines.append(f"⚠️ Review {PLAT_NAMES[worst_plat]} — CPL cao hơn {(worst_cpl/best_cpl-1)*100:.0f}% vs best")
    if creative_alerts:
        lines.append("🔄 Chuẩn bị creative mới cho platform có dấu hiệu fatigue")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────
def main(state: HandState, logger: HandLogger):
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["weekly", "monthly"], default="weekly")
    args, _ = parser.parse_known_args()

    secrets = load_secrets()
    sb_url = secrets["report_sb_url"]
    sb_key = secrets["report_sb_key"]

    if args.mode == "monthly":
        cur_range, prev_range = get_monthly_ranges()
        logger.info(f"Monthly review: {cur_range[0]} → {cur_range[1]}")
    else:
        cur_range, prev_range = get_weekly_ranges()
        logger.info(f"Weekly review: {cur_range[0]} → {cur_range[1]}")

    logger.info("Fetching current period data...")
    cur_rows = fetch_range(sb_url, sb_key, *cur_range)

    logger.info("Fetching previous period data...")
    prev_rows = fetch_range(sb_url, sb_key, *prev_range)

    if not cur_rows:
        logger.info("No data for current period — skip")
        send_telegram(f"📊 Weekly/Monthly Review: Không có dữ liệu kỳ {cur_range[0]} → {cur_range[1]}")
        return

    cur_agg = aggregate(cur_rows)
    prev_agg = aggregate(prev_rows)
    creative_alerts = detect_creative_fatigue(cur_agg)

    message = build_report(args.mode, cur_range, prev_range, cur_agg, prev_agg, creative_alerts)

    logger.info("Sending Telegram report...")
    send_telegram(message)
    logger.info("Done.")


if __name__ == "__main__":
    state = HandState.load(HAND_NAME)
    logger = HandLogger(HAND_NAME)
    steps = [
        {"name": "main", "fn": lambda: main(state, logger), "skip_if_done": False}
    ]
    run_hand(HAND_NAME, steps, state, logger)
