---
name: ads-anomaly
description: Tự động phát hiện CPM/CPC/Spend bất thường trong ngày so với 7 ngày trước và gửi alert Telegram khi có dấu hiệu anomaly. Use when cần monitor bất thường ads để chặn thất thoát ngân sách sớm.
---

# Ads Anomaly

## Operational Notes

- Cron: `0 */2 * * *` (mỗi 2 tiếng, chạy cả ngày)
- Script: `python3 skills/ads-anomaly/scripts/ads_anomaly.py`
- Dedup alert key: `{platform}_{metric}_{date}`
- Config: `skills/ads-anomaly/config/defaults.json`

## Config

File `config/defaults.json` chứa:
- **thresholds**: CPM/CPC % change (default 30%), Spend % change (default 50%), min sample days (3), min sample value (5)
- **retry**: max retries (2), delay (5s), timeout (20s) — áp dụng cho tất cả API calls
- **alert**: daily summary hour ICT (21h), max alerts per day (10)

## Retry Policy

Mỗi HTTP request được wrap bởi `_request_with_retry()`:
- Retry on: HTTP 500+, Timeout, ConnectionError
- Linear backoff: delay × (attempt + 1)
- Fetch functions vẫn return None nếu tất cả retries fail (graceful fallback)

## Confidence Guard

Anomaly check bỏ qua khi:
- History < `min_sample_days` ngày (default 3)
- Average value < `min_sample_value` (default 5) — tránh noise

## Daily Summary

- Gửi 1 tin tổng hợp lúc 21h ICT (configurable)
- Chỉ gửi nếu có anomalies trong ngày
- Reset tự động khi sang ngày mới

## Alert Capping

- Max alerts/day: 10 (configurable)
- Slot-based: nếu đã gửi 8, chỉ còn 2 slots
- Log warning khi bị cap

## Credentials

- `credentials/fb_token.txt`
- `credentials/report_ads_secrets.json` (tt_token, tt_adv, gg_config, gg_account)
- `credentials/telegram_token.txt`

## Category
marketing-ads

## Trigger

Use this skill when:
- Cần phát hiện bất thường trong dữ liệu quảng cáo
- CPM/CPC/CTR tăng/giảm đột biến
- Cron alert kiểm tra ads định kỳ
- User says: "check ads bất thường", "CPM tăng đột biến", "kiểm tra anomaly ads"
