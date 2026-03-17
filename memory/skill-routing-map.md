# Skill Routing Map
> Last updated: 2026-03-17 | Em đọc file này khi cần chọn skill cho task

---

## Lookup Table — Chọn theo task type

| Task type | Skill ưu tiên | Fallback | Ghi chú |
|-----------|--------------|---------|---------|
| Search / research web | `search-kit` | `web_search` built-in | search-kit dùng Perplexity, tiết kiệm hơn |
| Viết SEO outline | `seo-outline` | `seo-article` (lite mode) | mặc định lite để tránh quá dài |
| Viết SEO bài đầy đủ | `seo-article` | — | có param brand/sector/location |
| Phân tích ads FB/TikTok/Google | `ads-insight-auto` | `report-ads` | insight-auto có baseline so sánh 7 ngày |
| Report ads hằng ngày | `report-ads` | — | lưu vào Supabase Report Storage |
| Weekly/monthly ads review | `weekly-review-auto` | — | cron thứ 2 8h (weekly), ngày 1 (monthly) |
| Chạy code phức tạp / untrusted | `daytona-sandbox` | `exec` local (nếu safe) | sandbox cho IPv6 + isolation |
| Tạo ảnh từ prompt | `creimage` | — | model gemini-3-pro-image |
| Lưu/tìm media (ảnh/video/audio) | `drive-media` | — | có SQLite index |
| Transcript video/audio | `sumvid` | — | Groq Whisper |
| Tạo content từ YouTube/Shorts | `yt-content` | `sumvid` | download → transcript → caption/SEO |
| Monitor lead realtime | `lead-monitor` | — | check Supabase status_data |
| Phát hiện anomaly ads | `ads-anomaly` | — | so sánh 7 ngày |
| Check budget pace | `ads-budget-pacing` | — | alert over/under-spend |
| A/B test tracking | `ab-test-tracker` | — | |
| Creative fatigue detection | `creative-fatigue-detector` | `ads-anomaly` | CTR giảm liên tiếp |
| Ads data contract/quality | `ads-data-contract` | — | enforce schema + quality checks |
| Task phức tạp nhiều bước (>5) | `aot-planner` → `aot-executor` | multi-agent manual | planner trước, executor sau |
| Review/QA quan trọng | `debate-review` | `clarity-gate-lite` | debate khi risk cao |
| Viết copy/headline/CTA | `copywriting` | — | |
| SEO keyword cluster / internal link | `programmatic-seo-lite` | — | |
| Comment FB Page DND | `fb-page-comment` | — | có template + ảnh Drive |
| Seeding comment FB Page | `fb-page-seeding-comment` | — | seeding comments tự động |
| LinkedIn auto-post/engage | `linkedin` | — | |
| Gợi ý trả lời inbox DND | `suggestion-reply-dnd` | — | học từ lịch sử inbox |
| Kiểm tra thông tin thị trường (giá vàng/crypto/chứng khoán) | `market-data` | `web_search` | enforce timestamp + source |
| Scrape web nâng cao | `reader-adapter` | `web_fetch` | reader cho content sạch hơn |
| Lưu article vào KB / search KB | `rag-kit` | — | |
| Lưu/search structured memory | `persistent-memory` | `smart-memory` | shelf-based, searchable |
| Smart memory (fact extraction) | `smart-memory` | `persistent-memory` | structured facts có TTL + dedup |
| Semantic memory search | `semantic-memory-search` | `persistent-memory` | search ngữ nghĩa |
| Track KPI leads/inbox | `kpi-tracker` | — | Supabase + Telegram alert |
| Tạo/update Apps Script | `apps-script-deployer-lite` | — | |
| Create thumbnail Thành Hưng | `thumb-prj-thanhhung` | — | Pillow replace text |
| Phân tích brand/website | `brand-analyze` | — | |
| Phân tích Messenger ads | `analyze-mess-ads` | — | group doctor/UGC/promo |
| Topic performance FB Ads | `topic-performance` | — | top creative topics, cron 8h15 ICT |
| Content factory (nhiều bài) | `content-factory` | `seo-article` | batch viết content |
| Backup workspace encrypted | `openclaw-backup` | — | AES-256-CBC → Google Drive |
| Memory tiering (hot/warm/cold) | `memory_tier` (tool) | — | classify + archive old files |
| API key rotation | `api_key_rotator` (tool) | — | auto-rotate khi rate limit |
| Ngôn ngữ thích ứng user | `adaptive-language` | — | tự chuyển VN/EN theo context |
| Context helper cho task | `context-help` | `lazy-context` | inject context tự động |
| Lazy context (on-demand) | `lazy-context` | — | load context khi cần |
| Context warning (drift alert) | `context-warning` | — | cảnh báo task drift |
| Error giải thích dễ hiểu | `error-translator` | — | dịch error message |
| Decision extractor | `decision-extractor` | — | extract decisions → memory |
| Session metrics tracking | `session-metrics` | — | turns, files, tools, drift |
| Recap session | `recap` | `persistent-memory` | tóm tắt session/topic |
| Progress tracker | `progress-tracker` | — | track task progress |
| Plan validation | `plan-validation-lite` | — | verify plan trước khi execute |
| Plans kanban | `plans-kanban-lite` | — | kanban-style task board |
| React loop (iterative) | `react-loop` | — | ReAct pattern cho multi-step |
| Next action suggestion | `next` | — | suggest next steps |
| Auto-save workspace | `auto-save` | `snapshot-ttl` | tự lưu state định kỳ |
| Snapshot + TTL cleanup | `snapshot-ttl` | — | manage snapshots, prune stale |
| Notify on task complete | `notify-on-complete-lite` | — | alert khi xong task |
| Prompt injection guard | `prompt-injection-guard` | — | detect + block injections |
| Guardrail hooks | `guardrail-hooks-lite` | — | pre/post-exec validation |
| Credentials health check | `credentials-health-lite` | — | check API keys còn valid |
| Skill catalog audit | `skill-catalog-audit-lite` | — | audit skills, tìm overlap/gap |
| Test orchestrator | `test-orchestrator-lite` | — | compile/lint/smoke gate |
| Workflow test checklist | `workflow-test-checklist-lite` | — | end-to-end workflow testing |
| Parallel file ownership | `parallel-file-ownership-lite` | — | manage file locks multi-agent |
| Antrua (internal tool) | `antrua` | — | |
| Hands framework (library) | `hands-framework` | — | import HandState/HandLogger |

---

## Routing Rules nhanh

```
Anh hỏi thông tin web     → search-kit (không dùng web_search trực tiếp)
Anh muốn viết content     → seo-outline trước → seo-article sau
Anh hỏi về ads performance → ads-insight-auto (có context 7 ngày)
Cần chạy Python phức tạp  → daytona-sandbox (IPv6 + isolation)
Task > 5 bước phức tạp    → aot-planner breakdown trước
Output sẽ publish/gửi KH  → clarity-gate-lite hoặc debate-review trước khi done
Cần lưu thông tin lâu dài → persistent-memory hoặc smart-memory
Anh gửi link YouTube      → yt-content (transcript + content)
Backup khi cần             → openclaw-backup (encrypted)
Review skills coverage     → skill-catalog-audit-lite
```

---

## Skills cần credentials (check trước khi dùng)

| Skill | Credentials cần | TTL / Note |
|-------|----------------|-----------|
| `report-ads` / `ads-insight-auto` / `weekly-review-auto` / `topic-performance` | FB token, TikTok token, Google Ads | FB token hết hạn ~21/04/2026 ⚠️ |
| `creimage` | minai93 API key | — |
| `sumvid` / `yt-content` | Groq API key | — |
| `apps-script-deployer-lite` | Google OAuth (ga_gsc_token) | — |
| `drive-media` / `openclaw-backup` | Google OAuth (workspace token) | — |
| `kpi-tracker` / `lead-monitor` | Supabase DND + Telegram | — |
| `search-kit` | Perplexity key ($5/tháng budget) | Check budget trước |

---

*File này do Ní maintain. Update khi có skill mới hoặc routing thay đổi.*
