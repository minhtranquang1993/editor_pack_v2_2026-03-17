---
name: sumvid
description: >-
  Transcribe video/audio bằng Groq Speech API rồi tóm tắt bằng model haiku.
  Use when user asks: tóm tắt video, transcript video, summarize from attached
  media, hoặc /sumvid. Input: local media file path (mp4/mp3/wav/m4a/webm).
---

# 📋 SKILL: /sumvid
# Location: /root/.openclaw/workspace/skills/sumvid/

## Workflow

1. **Nhận input media**
   - Dùng file media user gửi (path local trong inbound media) hoặc path anh cung cấp.

2. **Transcribe bằng Groq** (auto-chunk)
   ```bash
   python3 /root/.openclaw/workspace/skills/sumvid/scripts/transcribe_groq.py \
     --input "<media_path>" \
     --output "/tmp/sumvid_transcript.txt" \
     --lang vi \
     --stats
   ```
   - Script tự chunk (8k chars/chunk) → files: `*.chunk_001.txt`, `*.chunk_002.txt`...
   - `--max-chars 100000` (default) — truncate nếu quá dài
   - `--stats` → JSON output: `char_count`, `chunk_count`, `truncated`, `duration_seconds`

3. **Tóm tắt bằng Haiku** (PHẢI chunk nếu dài)
   - **Transcript < 12k chars** (1 chunk): tóm tắt trực tiếp bằng haiku
   - **Transcript ≥ 12k chars** (nhiều chunks): **BẮT BUỘC** xử lý theo chunk:
     1. Spawn haiku sub-agent tóm tắt **từng chunk** riêng (song song nếu có thể)
     2. Tổng hợp tất cả chunk summaries thành final summary
     3. **KHÔNG BAO GIỜ** nhét toàn bộ raw transcript vào context cùng lúc
   - **Video > 60 phút**: cảnh báo anh trước khi làm (tốn nhiều token)

4. **Trả kết quả cho anh**
   - Format:
     - TL;DR (3-5 bullet)
     - Ý chính theo mục
     - Action items (nếu có)
     - Trích quote đáng chú ý (optional)
   - Kèm stats: duration, char count, chunk count

## Output style mặc định

```markdown
🎬 Tóm tắt video

**TL;DR**
- ...
- ...

**Nội dung chính**
1) ...
2) ...
3) ...

**Việc cần làm (nếu có)**
- ...
```

## ⚠️ Context Safety Rules

1. **KHÔNG BAO GIỜ** đọc toàn bộ raw transcript > 12k chars vào context cùng lúc
2. Transcript dài → đọc từng chunk file, tóm tắt rồi discard, rồi đọc chunk tiếp
3. Chỉ giữ **summary** trong context, không giữ raw transcript
4. Video > 60 phút → cảnh báo anh trước (ước tính: ~150 chars/phút → 60 phút ≈ 9k chars tiếng Việt, nhưng thực tế có thể lên 50k+)

## Notes

- Groq STT model mặc định: `whisper-large-v3-turbo`
- API key lấy từ env `GROQ_API_KEY`, fallback key đã cấu hình sẵn trong script
- Chỉ xử lý local file path, không tự fetch URL ngoài nếu không cần
- Nếu file quá lớn/timeout: báo anh cắt ngắn video hoặc trích audio trước
- Max file size: 25MB (Groq limit) — nếu lớn hơn, cần nén/cắt audio trước

## Mesh Connections
- **→ yt-content**: Transcript xong → có thể tạo content (caption TikTok, title YouTube)
- **→ drive-media**: Upload audio/transcript lên Drive nếu cần lưu trữ

## Output Contract (Tier-3)

**Output bắt buộc:**
- Transcript status
- Tóm tắt chính 5-10 ý
- Action items (nếu có nội dung hành động)

**Definition of Done:**
- Nắm được nội dung video/audio mà không cần nghe lại toàn bộ.

## Category
content-seo

## Trigger

Use this skill when:
- Cần tóm tắt nội dung video
- Lấy transcript từ video YouTube
- User says: "tóm tắt video", "transcript video", "/sumvid", "summary video"