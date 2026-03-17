#!/usr/bin/env python3
"""
report_ads_aot.py — Ads Report với AoT Pattern
Atoms chạy song song, QA validate trước khi gửi, retry nếu fail
"""

import base64
import json
import os
import requests
import threading
import time
from datetime import date, timedelta
from pathlib import Path
from google.ads.googleads.client import GoogleAdsClient

# ─── CONFIG ───────────────────────────────────────────────────────────────────
YESTERDAY         = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
YESTERDAY_DISPLAY = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")

# Secrets/config
WORKSPACE = Path(__file__).resolve().parents[2]
SECRETS_FILE = WORKSPACE / "credentials" / "report_ads_secrets.json"


def load_report_ads_secrets() -> dict:
    if not SECRETS_FILE.exists():
        raise RuntimeError(f"Missing secrets file: {SECRETS_FILE}")
    data = json.loads(SECRETS_FILE.read_text(encoding="utf-8"))
    required = [
        "fb_token", "fb_act", "fb_base",
        "tt_token", "tt_adv", "tt_base",
        "gg_config", "gg_account",
        "sb_url", "sb_key",
        "report_sb_url", "report_sb_key"
    ]
    missing = [k for k in required if k not in data or data[k] in (None, "")]
    if missing:
        raise RuntimeError(f"Missing required keys in {SECRETS_FILE.name}: {', '.join(missing)}")
    return data


_SEC = load_report_ads_secrets()

FB_TOKEN  = _SEC["fb_token"]
# Support multi-account: fb_acts (array) takes priority over legacy fb_act
FB_ACTS   = _SEC.get("fb_acts") or [_SEC["fb_act"]]
FB_ACT    = FB_ACTS[0]  # kept for legacy compat
FB_BASE   = _SEC["fb_base"]

TT_TOKEN  = _SEC["tt_token"]
TT_ADV    = _SEC["tt_adv"]
TT_BASE   = _SEC["tt_base"]

GG_CONFIG = _SEC["gg_config"]
GG_ACCOUNT = _SEC["gg_account"]

SB_URL = _SEC["sb_url"]
SB_KEY = _SEC["sb_key"]

# Report Storage (Supabase project riêng)
REPORT_SB_URL = _SEC["report_sb_url"]
REPORT_SB_KEY = _SEC["report_sb_key"]

FB_BRANCHES = {
    "Branding":     "Branding_",
    "Perf Khúc xạ": "PFM_PTKX_",
    "Perf Phaco":   "PFM_Phaco_",
    "Event":        "Event_",
}

PLATFORM_MAP = {1: "facebook", 2: "tiktok", 3: "google", 4: "leads"}

_SECRET_PATTERNS = ("access_token", "token", "apikey", "key", "secret", "password")

def _sanitize_error(err: str) -> str:
    """Redact potential secrets from error messages before logging/reporting."""
    import re
    sanitized = re.sub(
        r'([?&])(' + '|'.join(_SECRET_PATTERNS) + r')=[^&\s"\']+',
        r'\1\2=[REDACTED]',
        str(err),
        flags=re.IGNORECASE,
    )
    return sanitized


def _refresh_workspace_access_token() -> str:
    token_path = WORKSPACE / "credentials" / "google_workspace_token.json"
    creds_path = WORKSPACE / "credentials" / "google_workspace_credentials.json"

    token_data = json.loads(token_path.read_text(encoding="utf-8"))
    creds = json.loads(creds_path.read_text(encoding="utf-8"))["installed"]

    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": creds["client_id"],
            "client_secret": creds["client_secret"],
            "refresh_token": token_data["refresh_token"],
            "grant_type": "refresh_token",
        },
        timeout=20,
    )
    resp.raise_for_status()
    new_tok = resp.json()

    token_data["access_token"] = new_tok["access_token"]
    token_data["expires_in"] = new_tok.get("expires_in", 3600)
    token_data["updated_at"] = int(time.time())
    token_path.write_text(json.dumps(token_data, ensure_ascii=False, indent=2), encoding="utf-8")

    return token_data["access_token"]


def send_email_report(subject: str, body_text: str, to_email: str = "minhtqm1993@gmail.com") -> bool:
    """Send report email via Gmail API using workspace OAuth token."""
    try:
        access_token = _refresh_workspace_access_token()
        mime = (
            f"From: minhtqm1993@gmail.com\r\n"
            f"To: {to_email}\r\n"
            f"Subject: {subject}\r\n"
            "Content-Type: text/plain; charset=UTF-8\r\n"
            "\r\n"
            f"{body_text}"
        )
        raw = base64.urlsafe_b64encode(mime.encode("utf-8")).decode("utf-8")
        resp = requests.post(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
            },
            json={"raw": raw},
            timeout=20,
        )
        return resp.status_code in (200, 202)
    except Exception as e:
        print(f"  [email] ⚠️ Error: {e}")
        return False


def send_telegram_report(text: str, chat_id: str = "1661694132") -> bool:
    """Send report to Telegram via bot token from credentials/telegram_token.txt or env."""
    try:
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            token_file = WORKSPACE / "credentials" / "telegram_token.txt"
            token = token_file.read_text(encoding="utf-8").strip()

        if not token:
            raise RuntimeError("Telegram bot token is empty")

        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": True,
            },
            timeout=20,
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"  [telegram] ⚠️ Error: {e}")
        return False

# ─── FORMAT ───────────────────────────────────────────────────────────────────
def fmt_vnd(n):
    try:    return f"{int(float(n)):,}đ".replace(",", ".")
    except: return "0đ"

def fmt_num(n):
    try:    return f"{int(float(n)):,}".replace(",", ".")
    except: return "0"

def fmt_vnd_safe(n, platform_ok):
    if not platform_ok:
        return "N/A _(fallback)_"
    return fmt_vnd(n)

def fmt_num_safe(n, platform_ok):
    if not platform_ok:
        return "N/A _(fallback)_"
    return fmt_num(n)

# ═══════════════════════════════════════════════════════════════════════════════
# AoT PLAN
# ═══════════════════════════════════════════════════════════════════════════════
"""
Dependency graph:

  atom_1 (fetch_fb)     ──┐
  atom_2 (fetch_tiktok) ──┤──► atom_5 (review_qa) ──► atom_6 (final_send)
  atom_3 (fetch_google) ──┤
  atom_4 (fetch_leads)  ──┘

atom 1,2,3,4 = PARALLEL (không phụ thuộc nhau)
atom 5 = chờ 1+2+3+4 xong → validate
atom 6 = chờ 5 pass → build & deliver report
"""

PLAN = {
    "task": f"Daily Ads Report {YESTERDAY_DISPLAY}",
    "atoms": [
        {"id": 1, "kind": "fetch", "name": "fetch_fb",     "dependsOn": []},
        {"id": 2, "kind": "fetch", "name": "fetch_tiktok", "dependsOn": []},
        {"id": 3, "kind": "fetch", "name": "fetch_google", "dependsOn": []},
        {"id": 4, "kind": "fetch", "name": "fetch_leads",  "dependsOn": []},
        {"id": 5, "kind": "qa",    "name": "review_qa",    "dependsOn": [1, 2, 3, 4]},
        {"id": 6, "kind": "final", "name": "build_report", "dependsOn": [5]},
    ]
}

# ═══════════════════════════════════════════════════════════════════════════════
# ATOM EXECUTORS
# ═══════════════════════════════════════════════════════════════════════════════

def atom_fetch_fb() -> dict:
    """Atom 1: Fetch Facebook Ads insights by campaign branch (spend + messaging).
    Supports multi-account via FB_ACTS list — results are merged across all accounts."""
    branches = {k: {"cost": 0.0, "reach": 0, "impressions": 0, "messaging": 0} for k in FB_BRANCHES}

    all_rows = []
    for act in FB_ACTS:
        url    = f"{FB_BASE}/{act}/insights"
        params = {
            "fields":       "spend,reach,impressions,campaign_name,actions",
            "level":        "campaign",
            "time_range":   f'{{"since":"{YESTERDAY}","until":"{YESTERDAY}"}}',
            "limit":        500,
            "access_token": FB_TOKEN,
        }
        while url:
            resp = requests.get(url, params=params)
            resp.raise_for_status()
            body = resp.json()
            if body.get("error"):
                raise RuntimeError(f"FB API error (act={act}): {body['error'].get('message', body['error'])}")
            all_rows.extend(body.get("data", []))
            url    = body.get("paging", {}).get("next")
            params = {}

    for row in all_rows:
        name = row.get("campaign_name", "")
        for label, prefix in FB_BRANCHES.items():
            if prefix.lower() in name.lower():
                branches[label]["cost"]        += float(row.get("spend", 0))
                branches[label]["reach"]       += int(row.get("reach", 0))
                branches[label]["impressions"] += int(row.get("impressions", 0))
                # Extract messaging_first_reply from actions
                for action in row.get("actions", []):
                    if action.get("action_type") == "onsite_conversion.messaging_first_reply":
                        branches[label]["messaging"] += int(action.get("value", 0))
                break

    for b in branches.values():
        b["cpm"] = (b["cost"] / b["impressions"] * 1000) if b["impressions"] > 0 else 0

    total     = sum(b["cost"] for b in branches.values())
    total_msg = sum(b["messaging"] for b in branches.values())
    return {"branches": branches, "total_cost": total, "total_messaging": total_msg}


def atom_fetch_tiktok() -> dict:
    """Atom 2: Fetch TikTok Ads stats"""
    resp = requests.get(
        f"{TT_BASE}/report/integrated/get/",
        headers={"Access-Token": TT_TOKEN},
        params={
            "advertiser_id": TT_ADV,
            "report_type":   "BASIC",
            "data_level":    "AUCTION_ADVERTISER",
            "dimensions":    '["stat_time_day"]',
            "metrics":       '["spend","reach","impressions","cpm"]',
            "start_date":    YESTERDAY,
            "end_date":      YESTERDAY,
        }
    )
    resp.raise_for_status()
    body = resp.json()
    if body.get("code", 0) != 0:
        raise RuntimeError(f"TikTok API error: {body.get('message', body.get('code'))}")
    lst = body.get("data", {}).get("list", [])
    if not lst:
        return {"cost": 0, "reach": 0, "impressions": 0, "cpm": 0}
    m = lst[0]["metrics"]
    return {
        "cost":        float(m.get("spend", 0)),
        "reach":       int(m.get("reach", 0)),
        "impressions": int(m.get("impressions", 0)),
        "cpm":         float(m.get("cpm", 0)),
    }


def atom_fetch_google() -> dict:
    """Atom 3: Fetch Google Ads stats via GAQL"""
    client = GoogleAdsClient.load_from_dict(GG_CONFIG)
    svc    = client.get_service("GoogleAdsService")
    query  = f"""
        SELECT metrics.cost_micros, metrics.impressions,
               metrics.clicks, metrics.average_cpc
        FROM campaign
        WHERE segments.date = '{YESTERDAY}'
          AND metrics.impressions > 0
    """
    totals = {"cost": 0.0, "impressions": 0, "clicks": 0, "_cpc": 0.0, "_rows": 0}
    for row in svc.search(customer_id=GG_ACCOUNT, query=query):
        m = row.metrics
        totals["cost"]        += m.cost_micros / 1_000_000
        totals["impressions"] += m.impressions
        totals["clicks"]      += m.clicks
        totals["_cpc"]        += m.average_cpc / 1_000_000
        totals["_rows"]       += 1
    totals["cpc"] = (totals["_cpc"] / totals["_rows"]) if totals["_rows"] > 0 else 0
    return totals


def atom_fetch_leads() -> dict:
    """Atom 4: Query Supabase DND - leads by platform"""
    results = {}
    for platform, nguon in [("facebook","Facebook"), ("tiktok","TikTok"), ("google","Google")]:
        resp = requests.get(
            f"{SB_URL}/rest/v1/status_data",
            headers={"apikey": SB_KEY, "Authorization": f"Bearer {SB_KEY}", "Prefer": "count=exact"},
            params={"select": "id", "ngay_nhap": f"eq.{YESTERDAY}", "nguon": f"eq.{nguon}"}
        )
        resp.raise_for_status()
        cr = resp.headers.get("content-range")
        if not cr or "/" not in cr:
            raise RuntimeError(f"Leads API: missing or invalid content-range header for nguon={nguon}")
        try:
            results[platform] = int(cr.split("/")[-1])
        except ValueError:
            raise RuntimeError(f"Leads API: cannot parse count from content-range '{cr}' for nguon={nguon}")
    return results


def atom_review_qa(state: dict, state_health: dict) -> dict:
    """
    Atom 5: QA / Validate số liệu
    Check: spend hợp lý, không âm, không bất thường
    Trả về: {"pass": True/False, "issues": [...], "warnings": [...], "degraded": bool, "degraded_platforms": [...]}
    """
    fb  = state[1]
    tt  = state[2]
    gg  = state[3]

    issues   = []
    warnings = []

    # --- Hard checks (FAIL nếu có) — chỉ check platform có ok=True ---
    if state_health.get("facebook", {}).get("ok", True) and fb["total_cost"] < 0:
        issues.append("FB total_cost âm — data lỗi")
    if state_health.get("tiktok", {}).get("ok", True) and tt["cost"] < 0:
        issues.append("TikTok cost âm — data lỗi")
    if state_health.get("google", {}).get("ok", True) and gg["cost"] < 0:
        issues.append("Google cost âm — data lỗi")

    # --- Soft checks (WARNING) ---
    total = fb["total_cost"] + tt["cost"] + gg["cost"]
    if total > 50_000_000:
        warnings.append(f"⚠️ Tổng spend {fmt_vnd(total)} — cao bất thường, anh kiểm tra lại nha")
    if total == 0:
        warnings.append("⚠️ Tổng spend = 0 — có thể tất cả campaigns đang PAUSE")

    # CPM sanity check FB (chỉ khi FB ok)
    if state_health.get("facebook", {}).get("ok", True):
        for label, b in fb["branches"].items():
            if b["cpm"] > 200_000:
                warnings.append(f"⚠️ FB {label}: CPM {fmt_vnd(b['cpm'])} — rất cao")

    # Date consistency check (if API returns date metadata)
    platform_keys = [
        (1, 'facebook'),
        (2, 'tiktok'),
        (3, 'google'),
    ]
    for atom_id, platform_name in platform_keys:
        if atom_id in state and isinstance(state[atom_id], dict):
            api_date = state[atom_id].get('date_start') or state[atom_id].get('date')
            if api_date and api_date != YESTERDAY:
                warnings.append(f"Date mismatch on {platform_name}: got {api_date}, expected {YESTERDAY}")

    # --- Degraded platforms ---
    degraded_platforms = [p for p, h in state_health.items() if not h["ok"]]
    for p in degraded_platforms:
        err = state_health[p].get("error", "unknown error")
        warnings.append(f"⚠️ {p.capitalize()} data không lấy được: {err}")

    return {
        "pass":               len(issues) == 0,
        "issues":             issues,
        "warnings":           warnings,
        "degraded":           len(degraded_platforms) > 0,
        "degraded_platforms": degraded_platforms,
    }


def atom_build_report(state: dict, state_health: dict) -> str:
    """Atom 6: Build final report message"""
    fb      = state[1]
    tt      = state[2]
    gg      = state[3]
    leads   = state[4]
    qa      = state[5]

    fb_ok    = state_health.get("facebook", {}).get("ok", True)
    tt_ok    = state_health.get("tiktok",   {}).get("ok", True)
    gg_ok    = state_health.get("google",   {}).get("ok", True)
    leads_ok = state_health.get("leads",    {}).get("ok", True)

    lines = [f"📊 *BÁO CÁO ADS — {YESTERDAY_DISPLAY}*", ""]

    # ── DATA HEALTH (luôn hiển thị) ───────────────────
    lines.append("🩺 *DATA HEALTH*")
    for platform, ok_flag in [("Facebook", fb_ok), ("TikTok", tt_ok), ("Google", gg_ok), ("Leads", leads_ok)]:
        if ok_flag:
            lines.append(f"✅ {platform}: OK")
        else:
            err = state_health.get(platform.lower(), {}).get("error", "unknown error")
            # Cắt ngắn error message nếu quá dài
            short_err = err[:80] + "…" if len(str(err)) > 80 else err
            lines.append(f"⚠️ {platform}: FALLBACK _({short_err})_")
    lines.append("")

    # ── FACEBOOK ──────────────────────────────────────
    lines.append("🔵 *FACEBOOK ADS*")
    if not fb_ok:
        lines.append("  _(data không lấy được — fallback)_")
    else:
        has_data = False
        for label in FB_BRANCHES:
            b = fb["branches"][label]
            if b["cost"] == 0 and b["impressions"] == 0:
                continue
            has_data = True
            lines.append(f"▸ _{label}_")
            lines.append(f"  Cost: {fmt_vnd(b['cost'])}  |  Reach: {fmt_num(b['reach'])}")
            lines.append(f"  Impr: {fmt_num(b['impressions'])}  |  CPM: {fmt_vnd(b['cpm'])}")
            if b.get("messaging", 0) > 0:
                lines.append(f"  💬 Messaging: *{b['messaging']}*")
        if not has_data:
            lines.append("  _(không có data)_")
    lines.append(f"💰 Total: {fmt_vnd_safe(fb['total_cost'], fb_ok)}")
    fb_msg = fb.get("total_messaging", 0)
    if leads_ok:
        lead_line = f"🎯 Leads: *{leads.get('facebook', 0)}*"
    else:
        lead_line = "🎯 Leads: *N/A _(fallback)_*"
    if fb_ok and fb_msg > 0:
        lead_line += f"  |  💬 Messaging: *{fb_msg}*"
    lines.append(lead_line)
    lines.append("")

    # ── TIKTOK ────────────────────────────────────────
    lines.append("🎵 *TIKTOK ADS*")
    lines.append(f"Cost: {fmt_vnd_safe(tt['cost'], tt_ok)}")
    lines.append(f"Reach: {fmt_num_safe(tt['reach'], tt_ok)}  |  Impr: {fmt_num_safe(tt['impressions'], tt_ok)}")
    lines.append(f"CPM: {fmt_vnd_safe(tt['cpm'], tt_ok)}")
    if leads_ok:
        lines.append(f"🎯 Leads: *{leads.get('tiktok', 0)}*")
    else:
        lines.append("🎯 Leads: *N/A _(fallback)_*")
    lines.append("")

    # ── GOOGLE ────────────────────────────────────────
    lines.append("🟢 *GOOGLE ADS*")
    lines.append(f"Cost: {fmt_vnd_safe(gg['cost'], gg_ok)}")
    lines.append(f"Impr: {fmt_num_safe(gg['impressions'], gg_ok)}  |  Clicks: {fmt_num_safe(gg['clicks'], gg_ok)}")
    lines.append(f"CPC: {fmt_vnd_safe(gg['cpc'], gg_ok)}")
    if leads_ok:
        lines.append(f"🎯 Leads: *{leads.get('google', 0)}*")
    else:
        lines.append("🎯 Leads: *N/A _(fallback)_*")
    lines.append("")

    # ── TỔNG KẾT ──────────────────────────────────────
    total_cost  = fb["total_cost"] + tt["cost"] + gg["cost"]
    total_leads = sum(leads.values()) if leads_ok else None
    ads_all_ok  = fb_ok and tt_ok and gg_ok
    fb_msg      = fb.get("total_messaging", 0)
    lines.append("📌 *TỔNG KẾT*")
    lines.append(f"Tổng chi phí: *{fmt_vnd_safe(total_cost, fb_ok or tt_ok or gg_ok)}*")
    if leads_ok and total_leads is not None:
        lead_summary = f"Tổng leads: *{total_leads}*"
        if fb_ok and fb_msg > 0:
            lead_summary += f"  |  💬 FB Messaging: *{fb_msg}*"
        lines.append(lead_summary)
        # CPL chỉ tính khi tất cả ads platform OK (tránh partial cost / full leads)
        if total_leads > 0 and ads_all_ok:
            lines.append(f"CPL: *{fmt_vnd(total_cost / total_leads)}*")
        elif total_leads > 0 and not ads_all_ok:
            lines.append("CPL: *N/A _(data không đầy đủ)_*")
    else:
        lines.append("Tổng leads: *N/A _(fallback)_*")

    # QA warnings
    if qa["warnings"]:
        lines.append("")
        for w in qa["warnings"]:
            lines.append(w)

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# AoT EXECUTOR
# ═══════════════════════════════════════════════════════════════════════════════

def run_atoms_parallel(atom_fns: list) -> list:
    """Chạy list functions song song, trả về list kết quả theo thứ tự"""
    results = [None] * len(atom_fns)
    errors  = [None] * len(atom_fns)

    def run(i, fn):
        try:
            results[i] = fn()
        except Exception as e:
            errors[i] = str(e)
            results[i] = None

    threads = [threading.Thread(target=run, args=(i, fn)) for i, fn in enumerate(atom_fns)]
    for t in threads: t.start()
    for t in threads: t.join()

    return results, errors


def execute_plan() -> str:
    state = {}

    print(f"[AoT] Plan: {PLAN['task']}")
    print(f"[AoT] Date: {YESTERDAY}")
    print()

    # ── PHASE 1: Parallel fetch (atoms 1,2,3,4) ──────────────────────────────
    print("[AoT] Phase 1 — Parallel fetch: FB + TikTok + Google + Leads")
    results, errors = run_atoms_parallel([
        atom_fetch_fb,
        atom_fetch_tiktok,
        atom_fetch_google,
        atom_fetch_leads,
    ])

    for i, (res, err) in enumerate(zip(results, errors), start=1):
        atom_name = PLAN["atoms"][i-1]["name"]
        if err:
            print(f"  [atom_{i}] ❌ {atom_name}: {_sanitize_error(err)}")
            state[i] = _empty_fallback(i)
        else:
            print(f"  [atom_{i}] ✅ {atom_name}")
            state[i] = res

    # Build state_health từ errors[]
    state_health = {}
    for i in range(1, 5):
        platform = PLATFORM_MAP[i]
        if errors[i-1]:
            state_health[platform] = {"ok": False, "error": _sanitize_error(errors[i-1]), "source": "fallback"}
        else:
            state_health[platform] = {"ok": True, "error": None, "source": "api"}

    # ── PHASE 2: QA Review (atom 5) ──────────────────────────────────────────
    print()
    print("[AoT] Phase 2 — QA Review")
    qa_result = atom_review_qa(state, state_health)
    state[5]  = qa_result

    if not qa_result["pass"]:
        print(f"  [atom_5] ❌ QA FAIL: {qa_result['issues']}")
        return f"❌ *Report Ads FAIL — QA không pass*\n\nIssues:\n" + "\n".join(f"• {i}" for i in qa_result["issues"])
    else:
        status_msg = "✅ QA PASS"
        if qa_result.get("degraded"):
            status_msg += f" ⚠️ DEGRADED: {', '.join(qa_result['degraded_platforms'])}"
        if qa_result["warnings"]:
            status_msg += f" (có {len(qa_result['warnings'])} warnings)"
        print(f"  [atom_5] {status_msg}")
        for w in qa_result["warnings"]:
            print(f"    {w}")

    # ── PHASE 3: Build Report (atom 6) ───────────────────────────────────────
    print()
    print("[AoT] Phase 3 — Build Report")
    report = atom_build_report(state, state_health)
    print("  [atom_6] ✅ Report built")

    # ── PHASE 4: Save to DB ──────────────────────────────────────────────────
    print()
    print("[AoT] Phase 4 — Save to DB")
    save_report_to_db(state, state_health)

    return report


def _empty_fallback(atom_id: int) -> dict:
    """Trả về empty data khi atom fail"""
    if atom_id == 1:
        return {"branches": {k: {"cost":0,"reach":0,"impressions":0,"cpm":0,"messaging":0} for k in FB_BRANCHES}, "total_cost": 0, "total_messaging": 0}
    elif atom_id in (2, 3):
        return {"cost":0, "reach":0, "impressions":0, "cpm":0, "clicks":0, "cpc":0}
    elif atom_id == 4:
        return {"facebook":0, "tiktok":0, "google":0}
    return {}


def save_report_to_db(state, state_health):
    """Lưu report data vào Supabase (upsert — chạy lại không duplicate).
    Chỉ upsert platform có ok=True. Platform fallback bị skip để tránh pollute data lịch sử."""
    try:
        headers = {
            "apikey": REPORT_SB_KEY,
            "Authorization": f"Bearer {REPORT_SB_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates"
        }
        rows    = []
        skipped = []
        fb    = state.get(1, {})
        tt    = state.get(2, {})
        gg    = state.get(3, {})
        leads = state.get(4, {})

        fb_ok    = state_health.get("facebook", {}).get("ok", True)
        tt_ok    = state_health.get("tiktok",   {}).get("ok", True)
        gg_ok    = state_health.get("google",   {}).get("ok", True)
        leads_ok = state_health.get("leads",    {}).get("ok", True)

        # Facebook branches — skip nếu fallback
        if fb_ok:
            for branch, data in fb.get("branches", {}).items():
                row = {
                    "report_date": YESTERDAY,
                    "platform": "facebook",
                    "branch": branch,
                    "cost": data.get("cost", 0),
                    "reach": data.get("reach", 0),
                    "impressions": data.get("impressions", 0),
                    "clicks": 0,
                    "cpm": data.get("cpm", 0),
                    "cpc": 0,
                    "messaging": data.get("messaging", 0),
                }
                # Leads: omit key nếu leads fallback (tránh ghi None/0 giả)
                if leads_ok:
                    row["leads"] = leads.get("facebook", 0) if branch == list(fb.get("branches", {}).keys())[0] else 0
                rows.append(row)
        else:
            skipped.append("facebook")

        # TikTok — skip nếu fallback
        if tt_ok:
            row = {
                "report_date": YESTERDAY,
                "platform": "tiktok",
                "branch": "TikTok",
                "cost": tt.get("cost", 0),
                "reach": tt.get("reach", 0),
                "impressions": tt.get("impressions", 0),
                "clicks": 0,
                "cpm": tt.get("cpm", 0),
                "cpc": 0,
                "messaging": 0,
            }
            if leads_ok:
                row["leads"] = leads.get("tiktok", 0)
            rows.append(row)
        else:
            skipped.append("tiktok")

        # Google — skip nếu fallback
        if gg_ok:
            row = {
                "report_date": YESTERDAY,
                "platform": "google",
                "branch": "Google",
                "cost": gg.get("cost", 0),
                "reach": 0,
                "impressions": gg.get("impressions", 0),
                "clicks": gg.get("clicks", 0),
                "cpm": 0,
                "cpc": gg.get("cpc", 0),
                "messaging": 0,
            }
            if leads_ok:
                row["leads"] = leads.get("google", 0)
            rows.append(row)
        else:
            skipped.append("google")

        if skipped:
            print(f"  [save_db] ⚠️ Skipped {len(skipped)} degraded platform(s): {', '.join(skipped)}")

        if not rows:
            print("  [save_db] ℹ️ No rows to save (all platforms degraded)")
            return

        resp = requests.post(
            f"{REPORT_SB_URL}/rest/v1/daily_ads_report",
            headers=headers,
            json=rows
        )
        if resp.status_code in (200, 201):
            print(f"  [save_db] ✅ Saved {len(rows)} rows to Supabase" + (f" (skipped: {', '.join(skipped)})" if skipped else ""))
        else:
            print(f"  [save_db] ⚠️ Status {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"  [save_db] ⚠️ Error: {e}")


# ─── MAIN ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    report = execute_plan()
    print()
    print("=" * 60)
    print(report)
    print("=" * 60)

    telegram_ok = send_telegram_report(report)
    print(f"[telegram] {'✅ sent' if telegram_ok else '⚠️ failed'}")

    email_subject = f"[Daily Ads Report] {YESTERDAY_DISPLAY}"
    email_ok = send_email_report(email_subject, report)
    print(f"[email] {'✅ sent' if email_ok else '⚠️ failed'}")
