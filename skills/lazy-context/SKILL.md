---
name: lazy-context
description: Three-tier context loading strategy (critical/important/deep) for token efficiency. Use when handling long-running projects and you must balance recall quality with context cost.
---

# 📋 SKILL: Lazy-Load Context
# Location: /root/.openclaw/workspace/skills/lazy-context/

## Mô tả
Load context theo 3 tiers để tiết kiệm token.
Chỉ load thêm khi thực sự cần.

---

## 3 Tiers

| Tier | Token | Khi nào | Nội dung |
|------|-------|---------|----------|
| **Tier 1** CRITICAL | ~200 | Luôn luôn (session start) | identity, core preferences, current task |
| **Tier 2** IMPORTANT | ~800 | Khi làm task liên quan | decisions, pending tasks, recent changes |
| **Tier 3** CONTEXT | ~2000 | Khi cần deep dive | full history, errors, daily log |

---

## Tier 1 — Auto-inject khi session bắt đầu

Load từ `MEMORY.md` (phần About + Preferences) + `memory/session_state.json` (summary only):

```
## Session Context (Auto-loaded - Tier 1)
- Anh: Minh đại ca (Telegram ID: 1661694132)
- Project: {session.summary.current_feature}
- Task: {session.summary.current_task} ({progress}%)
- Next: {session.summary.next_step}
- Last saved: {updated_at}
```

**Token budget: ~200 tokens — luôn load, không hỏi.**

---

## Tier 2 — Load khi task liên quan

Trigger tự động khi:
- Anh hỏi về quyết định đã làm trước đây
- Anh tiếp tục task đang dở
- Anh hỏi về pending work

Load thêm từ `session_state.json`:
```
decisions_made[-5:]     → 5 quyết định gần nhất
pending_tasks[:5]       → 5 việc cần làm
recent_changes[-5:]     → 5 thay đổi gần đây
```

**Token budget: ~600 tokens thêm.**

---

## Tier 3 — Load khi deep dive

Trigger khi:
- Anh hỏi về lỗi cụ thể
- `/recap deep` được gọi
- Anh hỏi "hôm nay mình làm gì"

Load thêm:
```
session_state.json → errors_encountered, context_checkpoints
memory/YYYY-MM-DD.md → 30 dòng cuối
MEMORY.md → full file
```

**Token budget: ~1200 tokens thêm.**

---

## Token Budget Plan

```
Total context budget: ~200K tokens (sonnet)
├── System prompt + skills: ~15K (fixed)
├── Conversation history: ~150K (dynamic)
├── Lazy context load: ~10K max
│   ├── Tier 1: 200 (luôn luôn)
│   ├── Tier 2: 600 (on-demand)
│   └── Tier 3: 1200 (explicit)
└── Buffer: ~25K (safety)
```

---

## Load Decision Logic

```
Em tự quyết định load tier nào:

Tier 1 always:
→ Mọi session đều inject Tier 1 vào context đầu phiên

Tier 2 when:
→ "tiếp tục", "hôm qua làm gì", "task cũ", "pending"
→ Anh bắt đầu làm việc (không phải hỏi thông thường)

Tier 3 when:
→ /recap deep, "full context", "lỗi hôm qua"
→ Cần debug hoặc review lịch sử

KHÔNG load Tier 2/3 khi:
→ Câu hỏi thông thường (thời tiết, tin tức)
→ Task mới hoàn toàn không liên quan context cũ
→ Small talk
```

---

## Fallback

```
Nếu session_state.json không có:
→ Chỉ load MEMORY.md (Tier 1 fallback)

Nếu MEMORY.md quá lớn (>5KB):
→ Chỉ đọc phần "About Tui" + "Active Context" (đầu file)
```

## Category
memory-context
