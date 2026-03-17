---
name: lead-monitor
description: Tự động check Supabase status_data theo lịch trong giờ làm việc và alert Telegram khi có lead mới từ Facebook/TikTok/Google. Use when cần theo dõi lead realtime và cảnh báo sớm.
---

# Lead Monitor

## Operational Notes

- Cron: `*/30 0-15 * * *` (mỗi 30 phút, 0h–15h UTC = 7h–22h ICT)
- Script: `python3 skills/lead-monitor/scripts/lead_monitor.py`
- Batch alert: khi `>= 3` leads cùng lúc
- Config: `skills/lead-monitor/config/defaults.json`

## Fingerprint Dedupe

- Fingerprint = MD5(phone + source + time_bucket)[:12]
- Time bucket: round created_at to nearest `time_window_minutes` (default 60)
- Ordered list, FIFO eviction khi > 500 entries
- Deterministic: same lead → same fingerprint → no duplicate alert

## Backfill Guard

- Max alerts per check: 5 (configurable)
- Khi restart sau downtime, chỉ alert N leads gần nhất
- Gửi thông báo cooldown cho leads bị skip

## Health Ping

- Interval: mỗi 4 giờ (configurable)
- Message: "💚 Lead Monitor alive — N leads hôm nay (HH:MM ICT)"
- Giúp biết monitor còn sống hay đã chết silent

## Field Mapping

Đọc từ config, fallback theo thứ tự:
- Source: nguon → platform_ads → source
- Name: ten_khach_hang → ho_ten → name → customer_name
- Phone: so_dien_thoai → phone → sdt → phone_number

## Credentials

- `credentials/supabase_key.txt`
- `credentials/telegram_token.txt`

## Category
marketing-ads

## Trigger

Use this skill when:
- Cần kiểm tra lead mới từ Supabase
- Cron alert theo dõi leads định kỳ
- User says: "check lead mới", "có lead chưa", "lead alert", "theo dõi leads"
