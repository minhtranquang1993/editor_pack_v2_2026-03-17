# Skill Routing Map
> Last updated: 2026-03-10 | Em đọc file này khi cần chọn skill cho task

---

## Lookup Table — Chọn theo task type

| Task type | Skill ưu tiên | Fallback | Ghi chú |
|-----------|--------------|---------|---------|
| Search / research web | `search-kit` | `web_search` built-in | search-kit dùng Perplexity, tiết kiệm hơn |
| Viết SEO outline | `seo-outline` | `seo-article` (lite mode) | mặc định lite để tránh quá dài |
| Viết SEO bài đầy đủ | `seo-article` | — | có param brand/sector/location |
| Phân tích ads FB/TikTok/Google | `ads-insight-auto` | `report-ads` | insight-auto có baseline so sánh 7 ngày |
| Report ads hằng ngày | `report-ads` | — | lưu vào Supabase Report Storage |
| Chạy code phức tạp / untrusted | `daytona-sandbox` | `exec` local (nếu safe) | sandbox cho IPv6 + isolation |
| Tạo ảnh từ prompt | `creimage` | — | model gemini-3-pro-image |
| Lưu/tìm media (ảnh/video/audio) | `drive-media` | — | có SQLite index |
| Transcript video/audio | `sumvid` | — | Groq Whisper |
| Monitor lead realtime | `lead-monitor` | — | check Supabase status_data |
| Phát hiện anomaly ads | `ads-anomaly` | — | so sánh 7 ngày |
| Check budget pace | `ads-budget-pacing` | — | alert over/under-spend |
| A/B test tracking | `ab-test-tracker` | — | |
| Task phức tạp nhiều bước (>5) | `aot-planner` → `aot-executor` | multi-agent manual | planner trước, executor sau |
| Review/QA quan trọng | `debate-review` | `clarity-gate-lite` | debate khi risk cao |
| Viết copy/headline/CTA | `copywriting` | — | |
| SEO keyword cluster / internal link | `programmatic-seo-lite` | — | |
| Comment FB Page DND | `fb-page-comment` | — | có template + ảnh Drive |
| Kiểm tra thông tin thị trường (giá vàng/crypto/chứng khoán) | `market-data` | `web_search` | enforce timestamp + source |
| Scrape web nâng cao | `reader-adapter` | `web_fetch` | reader cho content sạch hơn |
| Lưu article vào KB / search KB | `rag-kit` | — | |
| Track KPI leads/inbox | `kpi-tracker` | — | Supabase + Telegram alert |
| Tạo/update Apps Script | `apps-script-deployer-lite` | — | |
| Create thumbnail Thành Hưng | `thumb-prj-thanhhung` | — | Pillow replace text |
| Phân tích brand/website | `brand-analyze` | — | |
| Phân tích Messenger ads | `analyze-mess-ads` | — | group doctor/UGC/promo |

---

## Routing Rules nhanh

```
Anh hỏi thông tin web     → search-kit (không dùng web_search trực tiếp)
Anh muốn viết content     → seo-outline trước → seo-article sau
Anh hỏi về ads performance → ads-insight-auto (có context 7 ngày)
Cần chạy Python phức tạp  → daytona-sandbox (IPv6 + isolation)
Task > 5 bước phức tạp    → aot-planner breakdown trước
Output sẽ publish/gửi KH  → clarity-gate-lite hoặc debate-review trước khi done
```

---

## Skills cần credentials (check trước khi dùng)

| Skill | Credentials cần | TTL / Note |
|-------|----------------|-----------|
| `report-ads` / `ads-insight-auto` | FB token, TikTok token, Google Ads | FB token hết hạn ~21/04/2026 ⚠️ |
| `creimage` | minai93 API key | — |
| `sumvid` | Groq API key | — |
| `apps-script-deployer-lite` | Google OAuth (ga_gsc_token) | — |
| `drive-media` | Google OAuth (workspace token) | — |
| `kpi-tracker` | Supabase DND + Telegram | — |
| `search-kit` | Perplexity key ($5/tháng budget) | Check budget trước |

---

*File này do Ní maintain. Update khi có skill mới hoặc routing thay đổi.*
