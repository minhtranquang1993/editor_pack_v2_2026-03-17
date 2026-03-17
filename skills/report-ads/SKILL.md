---
name: report-ads
description: Tự động tổng hợp chi phí quảng cáo Facebook/TikTok/Google, leads từ Supabase, build report và gửi qua Telegram/email. Use when cần báo cáo ads hằng ngày tự động.
---

# Report Ads

## Operational Notes

- Cron: `0 0 * * *` (0h00 UTC = 7h00 ICT)
- Script: `python3 skills/report-ads/report_ads_aot.py`
- Config: `skills/report-ads/references/output-contract.md`

## Module Structure

```
report-ads/
├── report_ads_aot.py          # Orchestrator (AoT runner)
├── atoms/                     # Data fetchers + QA
│   ├── fetch_fb.py            # Facebook Ads API
│   ├── fetch_tiktok.py        # TikTok Ads API
│   ├── fetch_google.py        # Google Ads API (lazy-load SDK)
│   ├── fetch_leads.py         # Supabase leads query
│   ├── review_qa.py           # QA validation + cross-checks
│   └── build_report.py        # Report builder + DataHealth class
├── delivery/                  # Delivery adapters
│   ├── telegram.py            # Telegram sender
│   └── email.py               # Email sender (stub)
├── references/
│   ├── README.md              # Architecture docs
│   └── output-contract.md     # Output format contract
└── scripts/
    └── smoke_test.py          # Pytest smoke tests
```

## Cross-Validation QA

- FB total = sum of branches (tolerance 1đ)
- Impressions > 0 nhưng cost = 0 → warning
- CPM > 200K → warning
- Cost < 0 → hard fail
- Date consistency: _source_date phải match YESTERDAY

## DataHealth (Centralized Fallback)

- `DataHealth.set_ok(platform)` / `DataHealth.set_fail(platform, error)`
- `DataHealth.fmt(value, platform)` → value hoặc "N/A _(fallback)_"
- Một nơi duy nhất quản lý platform health status

## Storage Write Guard

- Chỉ upsert rows có platform_ok = True
- Reject cost < 0
- Reject report_date != YESTERDAY

## Credentials

- `credentials/report_ads_secrets.json`
- `credentials/fb_token.txt`
- `credentials/telegram_token.txt`

## Category
marketing-ads

## Trigger

Use this skill when:
- Cần báo cáo quảng cáo đa nền tảng (FB/Google/TikTok)
- Báo cáo ads hàng ngày với QA validation
- User says: "báo cáo ads", "report FB/Google/TikTok hôm nay", "daily ads report"