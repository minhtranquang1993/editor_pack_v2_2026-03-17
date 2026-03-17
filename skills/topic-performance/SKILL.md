---
name: topic-performance
description: Mỗi sáng 8h15 ICT, gửi Telegram báo cáo top creative topics Facebook Ads hiệu quả nhất trong 3 ngày qua — dựa trên Mess (inbox) và Lead — để biết nên scale topic nào. Trigger: cron tự động hoặc manual "xem topic performance", "topic hôm nay".
---

# Skill: topic-performance

> Owner: Ní
> Status: production
> Created: 2026-03-12

## Mô tả

Mỗi sáng 8h15 ICT, gửi Telegram báo cáo top creative topics Facebook Ads hiệu quả nhất trong 3 ngày qua — dựa trên **Mess** (inbox) và **Lead** — để biết nên scale topic nào.

## Cron

```
15 1 * * *   # 8h15 ICT = 1h15 UTC
```

```bash
cd /root/.openclaw/workspace && python3 skills/topic-performance/scripts/topic_performance.py >> memory/hands/topic_performance/run.log 2>&1
```

## Data Sources

| Metric | Source | Detail |
|--------|--------|--------|
| Mess | FB Ads API | `onsite_conversion.messaging_first_reply` |
| Lead | Supabase `data` table | rows per `ad_id` + `created_at` |
| Topic map | Supabase `id_ads` table | `topic_content` field, filter `nen_tang_chay = Messenger` |

## Credentials Required

| File | Nội dung |
|------|----------|
| `credentials/supabase_dnd.json` | `{"sb_url": "...", "sb_key": "..."}` |
| `credentials/fb_token.txt` | Facebook Ads API access token |

## Config

Edit `skills/topic-performance/config.json` để thay đổi cấu hình:

```json
{
  "format_icon": {"VID": "🎬", "IMG": "🖼️"},
  "topic_labels": {
    "Bacsi.Tuan": "Bác sĩ Tuấn",
    "Bacsi.Quynh": "Bác sĩ Quỳnh",
    "Bacsi": "Bác sĩ",
    "UGC": "Review KH",
    "CTKM": "Khuyến mãi",
    "PR.HTV": "PR HTV",
    "PR.HV7": "PR HTV7",
    "PR": "PR",
    "HuongSmartSight": "Hương SmartSight"
  },
  "min_mess": 5,
  "days_back": 3
}
```

### Thêm topic mới

1. Mở `config.json`
2. Thêm entry vào `topic_labels`, ví dụ: `"NewTopic": "Tên hiển thị"`
3. Format topic_content trong Supabase: `{VID|IMG}.{TopicKey}`

**Config precedence:** `config.json` > hardcoded defaults trong script.

## CLI Flags

```bash
# Chạy bình thường (gửi Telegram)
python3 scripts/topic_performance.py

# Dry run — xem message mà không gửi
python3 scripts/topic_performance.py --dry-run

# Override ngày
python3 scripts/topic_performance.py --date 2026-03-10 --dry-run

# Bỏ qua dedup (gửi lại dù đã gửi hôm nay)
python3 scripts/topic_performance.py --force
```

## Dependencies

- `hands-framework` skill (`HandState`, `HandLogger`, `send_telegram`, `run_hand`)
- `requests` library
- Supabase REST API (no SDK)
- FB Graph API v21.0

## Troubleshooting

| Vấn đề | Nguyên nhân | Giải pháp |
|--------|-------------|-----------|
| "Token FB hết hạn" | FB access token expired | Refresh token và cập nhật `credentials/fb_token.txt` |
| "Không load được topic map" | Supabase `id_ads` table down hoặc credentials sai | Check Supabase dashboard, verify `credentials/supabase_dnd.json` |
| "Supabase lead data không khả dụng" | Supabase `data` table timeout | Script vẫn gửi partial report (chỉ mess). Leads sẽ hiển thị `—` |
| "Already sent today, skipping" | Dedup protection | Dùng `--force` để gửi lại |
| Không có data | Không có campaign Messenger active | Check FB Ads Manager |

## File Structure

```
skills/topic-performance/
├── SKILL.md              ← tài liệu này
├── config.json           ← externalized config (topic labels, thresholds)
└── scripts/
    ├── topic_performance.py   ← main script
    └── smoke_test.py          ← unit tests
```

## Category
marketing-ads
