---
name: session-metrics
description: >-
  Lightweight session metrics tracking. Auto-append stats vào daily log cuối session.
  Track: turns, files touched, tools called, decisions made, drift level.
---

# 📋 SKILL: Session Metrics Tracking
# Location: /root/.openclaw/workspace/skills/session-metrics/

## Mô tả

Track lightweight metrics trong session, auto-append vào daily log khi session kết thúc.
Chạy ngầm, không interrupt conversation.

---

## Metrics Tracked

```json
{
  "session_metrics": {
    "date": "2026-02-20",
    "start_time": "19:00 UTC",
    "end_time": "20:30 UTC",
    "turns": 0,
    "files_touched": [],
    "tools_called": {},
    "decisions_made": 0,
    "drift_level": "low",
    "tasks_completed": [],
    "context_warnings": 0,
    "agent_spawns": {
      "plan_opus": 0,
      "main_sonnet": 0,
      "sub_haiku": 0,
      "qa_codex": 0
    },
    "token_estimate": {
      "total": 0,
      "note": "single=1x, single+tools=~4x, multi-agent=~15x"
    }
  }
}
```

---

## Tracking Logic (Chạy ngầm mỗi turn)

### 1. `turns` — Đếm số lượt tin nhắn
```
Increment after each user message
```

### 2. `files_touched` — Files đã đọc/ghi
```
Mỗi khi em dùng read/write/edit tool:
→ Append filename vào files_touched (unique, không trùng)
→ Ví dụ: ["MEMORY.md", "memory/2026-02-20.md", "skills/recap/SKILL.md"]
```

### 3. `tools_called` — Tools được gọi bao nhiêu lần
```
Mỗi khi em gọi tool:
→ tools_called[tool_name] += 1
→ Ví dụ: {"read": 5, "write": 3, "exec": 8, "web_search": 2}
```

### 4. `decisions_made` — Số quyết định được ghi
```
Sync từ decision-extractor: đếm số entries trong session.json → decisions_made
```

### 5. `drift_level` — Bao lâu không cập nhật context
```
low:    < 10 turns kể từ lần cuối update session.json
medium: 10-20 turns
high:   > 20 turns không update

Tự động reset khi session.json được save
```

### 6. `tasks_completed` — Tasks đã xong trong session
```
Sync từ session.json → recent_changes (type: "completed")
```

### 7. `context_warnings` — Số lần cảnh báo context > 80%
```
Increment khi context-warning skill trigger
```

---

## Output Format — Cuối session

Khi detect user_leaving → auto-save → append vào `memory/YYYY-MM-DD.md`:

```markdown
---
📊 Session Stats — 2026-02-20 (19:00–20:30 UTC)
• Turns: 28 | Files: 7 | Tools: 15 calls | Decisions: 3
• Tools breakdown: read×6, write×5, exec×3, web_search×1
• Files touched: MEMORY.md, session.json, skills/recap/SKILL.md (+4 more)
• Drift: low ✅ | Context warnings: 0
• Tasks done: [Fix minai93 model ID, Implement 11 AWF features]
---
```

**Compact version** (default — 1 dòng):
```markdown
📊 Stats: 28 turns | 7 files | 15 tools | 3 decisions | drift: low
```

---

## Thêm vào session.json schema

```json
{
  "session_metrics": {
    "turns": 28,
    "files_touched": ["MEMORY.md", "session.json"],
    "tools_called": {"read": 6, "write": 5, "exec": 3},
    "decisions_made": 3,
    "drift_level": "low",
    "tasks_completed": ["Fix model ID", "Implement AWF skills"],
    "context_warnings": 0
  }
}
```

---

## Drift Detection

Inspired by HiveMind's drift score concept — adapted cho Ní:

```
drift_level = f(turns_since_last_session_update)

Sau mỗi save của session.json → reset drift counter
Mỗi turn không save → counter += 1

< 10 turns  → drift: low  ✅ (đang làm việc, context fresh)
10-20 turns → drift: med  ⚠️ (nên update session.json)
> 20 turns  → drift: high ❌ (cảnh báo: "Anh ơi, em chưa save context lâu rồi!")
```

**Cảnh báo drift high (1 lần mỗi session):**
```
⚠️ Context drift: Em chưa lưu session state 20+ turns rồi.
   Đang save ngay... 💾
```
→ Trigger auto-save luôn khi cảnh báo drift high.

---

## Integration

| Skill | Liên kết |
|-------|---------|
| auto-save | Trigger metrics append khi save |
| decision-extractor | Sync `decisions_made` count |
| context-warning | Increment `context_warnings` |
| snapshot-ttl | Metrics saved trong snapshot |

---

## Privacy

- Metrics chỉ lưu local (`memory/YYYY-MM-DD.md` + `session.json`)
- Không gửi ra ngoài
- Filenames trong `files_touched` → chỉ basename, không absolute path

## Category
memory-context
