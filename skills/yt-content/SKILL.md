---
name: yt-content
description: >-
  Tạo content từ video YouTube/Shorts: download audio → transcript (Deepgram) → viết caption TikTok + title/description SEO YouTube + hashtag.
  Trigger: "tạo content từ link youtube", "viết caption tiktok từ video", "transcript youtube", "làm content từ video", hoặc khi anh gửi link YouTube/Shorts kèm yêu cầu tạo content.
---

# yt-content Skill

## Workflow

```
Input: YouTube/Shorts URL
  │
  ├─ 1. Transcript trực tiếp từ YouTube URL — RapidAPI (KHÔNG cần tải audio)
  │     └─ Script tự chia chunks 8k chars + stats JSON
  ├─ 2. Fallback khi RapidAPI fail: Download audio (mp3) — yt-dlp + cookies
  ├─ 3. Transcript fallback — Deepgram nova-2 (tiếng Việt)
  │
  ├─ 4. Xử lý transcript (CHUNK-SAFE):
  │     ├─ < 12k chars → đọc trực tiếp
  │     └─ ≥ 12k chars → đọc từng chunk, tóm tắt, discard
  │
  ├─ 5. Viết caption TikTok (từ summary, KHÔNG từ raw transcript dài)
  ├─ 6. Viết title YouTube SEO
  ├─ 7. Viết description YouTube SEO
  └─ 8. Trả anh duyệt
```

## ⚠️ Context Safety Rules

1. **KHÔNG BAO GIỜ** đọc toàn bộ raw transcript > 12k chars vào context cùng lúc
2. Transcript dài → đọc chunk → tóm tắt → discard → đọc chunk tiếp
3. Viết content từ **summary**, không từ raw transcript dài
4. Video > 60 phút → cảnh báo anh trước khi làm

## References
- `references/style-dimensions-power-words.md` — Style Dimensions (TikTok caption profile) + Power Words tiếng Việt

## Cách chạy

### Bước 1 — Transcript trực tiếp từ YouTube URL (ưu tiên, không cần tải audio)
```bash
python3 skills/yt-content/scripts/yt_transcript.py \
  --youtube-url "<youtube_url>" \
  --output /tmp/yt_transcript.txt \
  --stats
```

### Bước 2 — Fallback: Download audio + transcript Deepgram (khi RapidAPI fail)
```bash
python3 skills/yt-content/scripts/yt_download.py \
  --url "<youtube_url>" \
  --output /tmp/yt_audio.mp3 \
  --cookies /tmp/yt_cookies.txt

python3 skills/yt-content/scripts/yt_transcript.py \
  --input /tmp/yt_audio.mp3 \
  --output /tmp/yt_transcript.txt \
  --stats
```
- Script tự chunk (8k chars/chunk) → files: `*.chunk_001.txt`, `*.chunk_002.txt`...
- `--stats` trả JSON: `provider`, `char_count`, `chunk_count`, `duration_seconds`, `truncated`
- RapidAPI keys có **auto-rotate + disable tạm theo TTL** khi dính quota/rate limit/forbidden → lần chạy sau tự xoay key khác
- Nếu `chunk_count > 1`: đọc từng chunk file, tóm tắt, rồi viết content từ summary

### Bước 3 — Viết content
Đọc transcript từ `/tmp/yt_transcript.txt`, xác định brand (xem `references/brand_profiles.md`), rồi viết:
1. **Caption TikTok** — hook mạnh + CTA + 3-5 hashtag, max 150 ký tự
2. **Title YouTube** — có keyword chính, max 70 ký tự
3. **Description YouTube** — 300-500 từ, chuẩn SEO, có CTA + thông tin liên hệ + hashtag

## Notes
- Cookies file: `/root/.openclaw/workspace/credentials/yt_cookies.txt` (persistent) — fallback `/tmp/yt_cookies.txt`
- Cookies hết hạn khi Google logout hoặc sau vài tuần → anh export lại từ Chrome gửi em là xong
- Deepgram key trong `scripts/yt_transcript.py`
- Brand profiles + hashtag pool: `references/brand_profiles.md`
- Output mặc định: private draft → anh duyệt → public
- Nếu yt-dlp báo JS challenge: đã config `--remote-components ejs:github` tự fix

## Output Contract (Tier-2)

**Output bắt buộc:**
- Transcript status: success/fallback/fail + nguồn (RapidAPI/Deepgram)
- TikTok caption
- YouTube title
- YouTube description
- Hashtag set

**Definition of Done:**
- Có đủ 4 output content kể cả khi transcript dùng fallback
- Nếu transcript fail hoàn toàn: phải báo rõ lý do + phương án xử lý

## Category
content-seo
