---
name: decision-extractor
description: Detect explicit/implicit user decisions and log them into session memory structure. Use when user confirms options, approves plans, or finalizes direction to keep decision history reliable.
---

# 📋 SKILL: Decision Extraction
# Location: /root/.openclaw/workspace/skills/decision-extractor/

## Mô tả
Tự động nhận diện khi anh đưa ra quyết định và ghi vào session_state.json.
Chạy ngầm, không cần anh nhắc.

## Session state chuẩn
- Ghi quyết định vào: `memory/session_state.json` -> `decisions[]`
- Schema tham chiếu: `config/session-state.schema.json`

---

## Trigger Patterns

Khi anh nói các phrase sau → tự động extract & save:

```
Quyết định rõ:
- "ok làm vậy", "chọn cái này", "dùng X", "theo X"
- "đồng ý", "confirm", "oke", "được rồi"
- "quyết định là", "mình sẽ dùng", "anh chọn"
- "thống nhất là", "chốt là"

Quyết định ngầm:
- Sau khi em propose → anh reply "ok" / "oke" / thumbs up
- Anh nói "implement đi" → quyết định theo plan em vừa đề xuất
- Anh approve một option cụ thể trong danh sách em đưa ra
```

---

## Extraction Logic

### Bước 1: Detect pattern trong tin nhắn anh

### Bước 2: Extract context
```
decision = {
  "timestamp": "[ISO datetime]",
  "decision": "[tóm tắt quyết định 1 dòng]",
  "context": "[đang bàn về gì]",
  "reason": "[lý do nếu anh có nêu]",
  "alternatives_rejected": "[option khác bị bỏ qua nếu có]"
}
```

### Bước 3: Append vào session_state.json
```json
{
  "decisions_made": [
    {
      "timestamp": "2026-02-20T19:00:00Z",
      "decision": "Dùng gpt-5.3-codex lowercase vì provider case-sensitive",
      "context": "Fix model ID trong openclaw config",
      "reason": "Provider minai93 case-sensitive với model ID",
      "alternatives_rejected": "GPT-5.3-Codex (uppercase)"
    }
  ]
}
```

### Bước 4: Silent — không thông báo cho anh
(Chỉ save ngầm, không làm interrupt conversation)

---

## Ví dụ thực tế

```
Conversation:
  Em: "Anh muốn dùng Exa hay Tavily cho search?"
  Anh: "Dùng Tavily đi, nhanh hơn"

→ Em tự extract:
  decision: "Dùng Tavily cho search task"
  context: "Chọn search engine"
  reason: "Nhanh hơn"
  alternatives_rejected: "Exa"

→ Append vào session_state.json silently ✅
```

```
Conversation:
  Em: "Em có 2 cách: A hoặc B"
  Anh: "Làm B đi"

→ Extract:
  decision: "Chọn phương án B"
  context: "[tên task đang làm]"
```

---

## Integration với /recap
Khi anh gọi `/recap full` → hiển thị `decisions_made[-5:]`
Anh có thể review lại các quyết định đã đưa ra.

---

## MEMORY.md Integration
Cuối session (khi detect user_leaving), extract decisions quan trọng:
- Quyết định về architecture / config
- Quyết định về workflow / process
→ Propose cho anh add vào MEMORY.md

## Category
memory-context
