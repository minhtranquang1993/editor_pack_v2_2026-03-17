---
name: recap
description: Recover working context at 3 detail levels (/recap, /recap full, /recap deep) or by topic. Use when resuming work, reorienting after interruption, or summarizing current status.
---

# 📋 SKILL: /recap — Context Recovery (3 Levels)
# Location: /root/.openclaw/workspace/skills/recap/

## ⚡ Quick Usage

| Command | Action |
|---------|--------|
| `/recap` | Tóm tắt nhanh session hiện tại (3-5 bullets) |
| `/recap full` | Chi tiết đầy đủ: tasks + decisions + blockers |
| `/recap deep` | Toàn bộ context: history + patterns + next actions |
| `/recap [topic]` | Recap theo chủ đề (e.g. `/recap ads`, `/recap seo`) |

**Alias:** `recap`, `/r`

## Mô tả
Khôi phục context với 3 mức độ để tiết kiệm token.

## Cách dùng
- `/recap` → Level 1: Nhanh (~200 tokens), chỉ summary
- `/recap full` → Level 1+2: Chi tiết (~800 tokens), kèm decisions + pending
- `/recap deep` → Level 1+2+3: Toàn bộ (~2000 tokens), kèm lỗi + history
- `/recap [topic]` → Smart search theo chủ đề

---

## Level 1 — Instant (Luôn load khi gọi /recap)

Đọc `memory/session_state.json` → field `summary`:

```
👋 Nhớ lại rồi!

📍 Project: {summary.project}
📍 Đang làm: {summary.current_feature}
   └─ Task: {summary.current_task}
   └─ Status: {summary.status} ({summary.progress_percent}%)

⏭️ Bước tiếp: {summary.next_step}
🕐 Last saved: {updated_at}

💡 Gõ /recap full để xem chi tiết hơn.
```

---

## Level 2 — On-Demand (khi gọi `/recap full`)

Đọc thêm từ `memory/session_state.json`:

```
─────────────────────────────
📋 Quyết định gần đây:
  {decisions_made[-5:]}

📝 Việc cần làm:
  {pending_tasks[:5]}

📁 Thay đổi gần đây:
  {recent_changes[-5:]}
─────────────────────────────
```

---

## Level 3 — Deep Dive (khi gọi `/recap deep`)

Đọc thêm:
- `memory/session_state.json` → errors_encountered, context_checkpoints
- `memory/YYYY-MM-DD.md` (today) → 30 dòng cuối

```
─────────────────────────────
🐛 Lỗi đã gặp:
  {errors_encountered}

💾 Checkpoints:
  {context_checkpoints[-5:]}

📜 Daily log hôm nay (30 dòng cuối):
  {tail -30 memory/YYYY-MM-DD.md}
─────────────────────────────
```

---

## Smart Search: `/recap [topic]`

Tìm kiếm trong:
1. `memory/session_state.json` → decisions, tasks, errors
2. `MEMORY.md` → long-term memory
3. `memory/YYYY-MM-DD.md` → daily logs (today + yesterday)

Chỉ load context liên quan đến topic → tiết kiệm token.

---

## Fallback

```
Nếu session_state.json không tồn tại:
→ "Chưa có session context. Em đọc MEMORY.md + daily log nhé!"
→ Load MEMORY.md + memory/YYYY-MM-DD.md

Nếu session_state.json bị lỗi:
→ Load snapshot mới nhất từ memory/snapshots/
→ "Đã khôi phục từ backup {date}."
```

## Category
memory-context

## Trigger

Use this skill when:
- Cần tóm tắt session làm việc trước đó
- Muốn biết hồi trước đã làm gì
- User says: "/recap", "tóm tắt session", "hồi trước làm gì", "recap"