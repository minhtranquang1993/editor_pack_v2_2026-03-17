---
name: weekly-review-auto
description: >-
  Tự động tổng hợp performance ads theo tuần/tháng từ Supabase, highlight top/bottom campaigns,
  creative alerts, budget recommendations, gửi report qua Telegram. Trigger: thứ 2 lúc 8h (weekly),
  ngày 1 tháng 8h (monthly), hoặc manual /weekly-review [weekly|monthly].
---

# weekly-review-auto

## Trigger & Schedule
- Weekly: Thứ 2 lúc 8h (UTC+7) — cron: `0 1 * * 1` (UTC)
- Monthly: Ngày 1 lúc 8h (UTC+7) — cron: `0 1 1 * *` (UTC)
- Manual: `/weekly-review weekly` hoặc `/weekly-review monthly`

## Workflow

### 1. Query Supabase
```sql
-- Weekly
SELECT * FROM daily_ads_report
WHERE report_date BETWEEN (NOW() - INTERVAL '7 days')::date AND NOW()::date
ORDER BY report_date DESC;

-- Monthly
SELECT * FROM daily_ads_report
WHERE date_trunc('month', report_date) = date_trunc('month', NOW())
ORDER BY report_date DESC;

-- Previous period (for comparison)
SELECT * FROM daily_ads_report
WHERE report_date BETWEEN (NOW() - INTERVAL '14 days')::date AND (NOW() - INTERVAL '7 days')::date;
```

### 2. Aggregate & Calculate
- Group by platform: sum cost, sum leads, avg cpm, avg cpc
- CPL = cost / leads (per platform)
- pct_change = (current - prev) / prev × 100
- Top 3 campaigns: sort by CPL asc (lowest CPL = best)
- Bottom 3 campaigns: sort by CPL desc or leads = 0
- Creative alerts: CTR trend giảm liên tiếp 3+ ngày

### 3. Build Report
Dùng template `references/report-template.md` (7 sections)

### 4. Send Telegram
```python
send_telegram(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode="MarkdownV2")
```

## Telegram Output Format
```
📊 *Weekly Review — Week {N}/{YYYY}*
📅 Generated: {DATE} 08:00

1️⃣ TỔNG CHI PHÍ — 2️⃣ LEADS & CPL — 3️⃣ TOP 3 — 4️⃣ BOTTOM 3 — 5️⃣ CREATIVE ALERTS — 6️⃣ BUDGET RECS — 7️⃣ ACTIONS
```

## Error Handling
- Supabase fail → retry 3x → log + skip
- Empty period → báo "Không có dữ liệu kỳ này"
- Missing field → default 0 hoặc N/A

## Dependencies
- supabase-py, python-telegram-bot, pandas, datetime
- Credentials: credentials/supabase_url.txt, credentials/supabase_key.txt, credentials/telegram_token.txt

## Category
marketing-ads

## Scripts

Hands-based script — chạy qua `run_hand()`.

```bash
python3 skills/weekly-review-auto/scripts/weekly_review.py [--mode weekly|monthly]
```

Key args:
- `--mode weekly` — (default) tổng kết 7 ngày gần nhất vs 7 ngày trước
- `--mode monthly` — tổng kết tháng hiện tại vs tháng trước

Workflow: Query Supabase → aggregate by platform → compare % change → detect creative fatigue → build report → send Telegram.
