---
name: kpi-tracker
description: Theo dõi tiến độ KPI leads + inbox Messenger theo tháng và gửi báo cáo định kỳ qua Telegram. Use when cần snapshot KPI nhanh hoặc theo dõi tiến độ KPI hằng ngày.
---

# KPI Tracker

## Operational Notes

- Cron: `30 9 * * *` (9h30 UTC = 16h30 ICT)
- Script: `python3 skills/kpi-tracker/scripts/kpi_tracker.py`
- On-demand: `python3 skills/kpi-tracker/scripts/kpi_tracker.py --date YYYY-MM-DD`
- Profile: `python3 skills/kpi-tracker/scripts/kpi_tracker.py --profile phaco`
- Config: `skills/kpi-tracker/config/kpi_config.json`

## Message Format (3 phần)

1. **SNAPSHOT**: Leads (FB/TikTok/Google), Tổng vs Pace, Inbox vs Pace, CPL, Cost
2. **RISK**: Forecast cuối tháng, Risk level (LOW/MEDIUM/HIGH), Needed/day
3. **ACTION**: Gợi ý hành động dựa trên risk level

Xem chi tiết: `references/message-template.md`

## Profile System

Config hỗ trợ nhiều profiles:
- Precedence: CLI `--profile` > env `KPI_PROFILE` > profiles.default > top-level (fallback)
- Profiles: default, phaco, khuc-xa (configurable)
- Backward compatible: nếu không có `profiles` section → dùng top-level targets

## Data Freshness Check

- Trước 10h ICT + leads = 0 → label "⏳ DATA TRỄ"
- Supabase error → label "⚠️ DATA LỖI"
- Tránh false alert khi data chưa sync

## Credentials

- `credentials/supabase_key.txt`
- `credentials/fb_token.txt`
- `credentials/telegram_token.txt`
- `credentials/kpi_tracker_secrets.json` (hoặc fallback `report_ads_secrets.json`)

## Category
marketing-ads

## Trigger

Use this skill when:
- Cần xem KPI hàng ngày/tuần
- Theo dõi tiến độ leads và metrics
- User says: "KPI hôm nay", "tiến độ leads", "báo cáo KPI", "KPI report"
