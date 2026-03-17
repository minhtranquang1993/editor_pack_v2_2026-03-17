---
name: semantic-memory-search
description: >-
  Smart search trên toàn bộ memory files. Dùng khi anh hỏi "hồi trước mình
  làm gì", "tìm quyết định về X", "search memory [keyword]". Kết hợp
  memory_search tool (built-in) + index.json để semantic + keyword search.
---

# 📋 SKILL: Semantic Memory Search
# Location: /root/.openclaw/workspace/skills/semantic-memory-search/

## Mô tả

Smart search trên tất cả memory files của Ní:
- `MEMORY.md` — long-term memory
- `memory/YYYY-MM-DD.md` — daily logs
- `memory/index.json` — structured mems (shelves/tags)
- `memory/session.json` — current session context

Không cần vector DB — dùng `memory_search` (built-in OpenClaw) + keyword matching trên `index.json`.

---

## Trigger

- Anh hỏi "hồi trước mình quyết định gì về X"
- Anh hỏi "lần trước fix lỗi Y như thế nào"
- Anh gõ `/recall_mems [keyword]`
- Anh hỏi "search memory về [topic]"
- Anh hỏi thứ gì đó mà em cần check memory trước khi trả lời

---

## Search Strategy — 3 tầng

### Tầng 1: index.json keyword search (nhanh nhất, ~instant)

```
Query index.json → mems[] → filter by:
  content.toLowerCase().includes(query)
  OR tags.some(t => t.includes(query))
  OR shelf === query

Sort: newest first
Return: top 5
```

### Tầng 2: memory_search tool (semantic, built-in OpenClaw)

```
Dùng memory_search tool với query → tìm trong MEMORY.md + memory/*.md
→ Trả về top snippets có path + line numbers
→ Combine với kết quả Tầng 1
```

### Tầng 3: Fallback grep (nếu 2 tầng trên không đủ)

```
read MEMORY.md → full text search
read memory/YYYY-MM-DD.md (today + yesterday) → full text search
```

---

## Output Format

### Có kết quả:
```
🔍 Tìm thấy {N} memories cho "{query}":

📌 [decisions] 2026-02-20
   minai93 provider case-sensitive — dùng gpt-5.3-codex lowercase
   Tags: openclaw, config, model-id

📌 [MEMORY.md#45]
   "...đã fix model ID: GPT-5.3-Codex → gpt-5.3-codex..."

💡 Muốn xem thêm? /recall_mems {query} shelf:errors
```

### Không có kết quả:
```
🔍 Không tìm thấy memory về "{query}".

Có thể thử:
• Query khác: "{query_suggestion}"
• /recall_mems (xem toàn bộ mems)
• /recap deep (load full context)
```

---

## Auto-search khi cần

Em tự động search memory TRƯỚC khi trả lời khi:
- Anh hỏi về config/API key → search `config` shelf
- Anh hỏi về lỗi đã gặp → search `errors` shelf
- Anh hỏi "anh thích/prefer cái gì" → search MEMORY.md
- Anh nhắc đến project/task cũ → search daily logs

**Không hỏi, không thông báo — tự search rồi dùng kết quả để trả lời chính xác hơn.**

---

## Ranking Logic

```
Score mỗi kết quả:
+10 nếu match trong tags (exact)
+8  nếu match trong content (exact)
+5  nếu match trong content (partial)
+3  nếu shelf match (exact)
+2  nếu newer (trong 7 ngày)
+1  nếu trong index.json (structured > prose)

Sort by score DESC → return top 5
```

---

## Integration với persistent-memory

`/recall_mems` gọi skill này làm backend.
Semantic Memory Search là core engine — persistent-memory là UI/UX layer.

## Category
memory-context
