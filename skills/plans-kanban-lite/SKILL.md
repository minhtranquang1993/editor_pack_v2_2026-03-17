---
name: plans-kanban-lite
description: Lightweight kanban planning for multi-step tasks. Use when a task has more than 3 steps, spans multiple sessions, or needs explicit status tracking (todo/in-progress/done/blocked) with clear next action.
---

# Plans Kanban Lite

Mục tiêu: quản lý task dài hơi bằng file markdown đơn giản, dễ đọc, dễ tiếp tục.

## Khi dùng
- Task > 3 bước
- Task kéo dài qua nhiều phiên
- Cần biết rõ đang kẹt ở đâu

## File location

Tạo file tại:
- `memory/plans/{yyyy-mm-dd}-{task-slug}.md`

## Template

```markdown
---
task: "..."
status: in-progress
owner: ni
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Backlog
- [ ] ...

## In Progress
- [ ] ...

## Blocked
- [ ] ... (reason: ...)

## Done
- [x] ...

## Next Action
- ...
```

## Operating rules

1. Mỗi lần hoàn thành 1 bước:
   - Move item sang `Done`
   - Update `updated`

2. Nếu bị kẹt:
   - Move item sang `Blocked`
   - Ghi rõ reason + cần gì để mở khóa

3. Luôn giữ `Next Action` chỉ 1 dòng cụ thể

4. Khi toàn bộ xong:
   - `status: done`

## Report format cho anh Minh

```text
📌 Plan update: [task]
- Done: X
- In Progress: Y
- Blocked: Z
- Next: ...
```

## Category
quality-ops

## Trigger

Use this skill when:
- Task có hơn 3 bước cần kanban tracking
- Cần visualize tiến độ dạng board
- User says: "kanban board", "track tiến độ", "tạo kanban", "task board"