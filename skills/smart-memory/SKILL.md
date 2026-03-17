---
name: smart-memory
description: >-
  Structured fact extraction + deduplication cho long-term memory chất lượng cao.
  Dùng khi: cần extract facts từ chat history, update smart memory sau session,
  check memory hiện tại, hoặc prune facts hết hạn. Trigger: /smart-memory,
  "cập nhật memory", "extract facts", "em nhớ gì về X", hoặc tự động sau mỗi ~20 tin nhắn quan trọng.
  Khác MEMORY.md (prose thô) — đây là structured facts có TTL, dedup, category.
---

# Smart Memory Skill

Extract + deduplicate facts từ chat → structured JSON memory với TTL tự động.

## Commands

```bash
# Extract facts từ messages (chạy sau session / mỗi ~20 msgs)
python3 scripts/extract_facts.py --messages '<json_array>'

# Xem toàn bộ memory hiện tại
python3 scripts/extract_facts.py --messages '[]' --list

# Preview trước khi save
python3 scripts/extract_facts.py --messages '<json_array>' --dry-run

# Dọn facts hết hạn
python3 scripts/extract_facts.py --messages '[]' --prune
```

## File output

`memory/smart-memory.json` — JSON array, auto-created nếu chưa có.

## Workflow chuẩn

1. **Thu thập messages** — lấy 15-25 tin nhắn gần nhất của session (bỏ qua heartbeat/system)
2. **Chạy extract** — Haiku phân tích, extract facts theo category
3. **Auto-dedup** — merge_key dedup tự động, giữ lịch sử nếu update
4. **TTL tự động** — fact_temp tự xóa sau 1 ngày, task_status sau 7 ngày, v.v.

## Categories & TTL

Xem `references/categories.md` để biết đầy đủ categories + TTL.

## Khi nào chạy

- Cuối session quan trọng (có quyết định / task mới)
- Sau mỗi ~20 tin nhắn có nội dung thực chất
- Khi anh hỏi "em nhớ gì về X" → list + filter by subject
- Khi heartbeat → prune expired facts

## Lưu ý

- Không lưu thông tin nhạy cảm (credentials, token) vào smart-memory — đã có MEMORY.md
- `confidence: low` → verify với anh trước khi dùng để ra quyết định
- Script cần `ANTHROPIC_API_KEY` env var để gọi Haiku

## Category
memory-context
