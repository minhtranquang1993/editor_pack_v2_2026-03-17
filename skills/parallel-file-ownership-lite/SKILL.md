---
name: parallel-file-ownership-lite
description: Parallel execution protocol with exclusive file ownership per phase. Use when multiple sub-agents run in parallel to avoid file conflicts and merge chaos.
---

# Parallel File Ownership Lite

Mục tiêu: chạy song song mà không đụng file nhau.

## Rule cứng
- Mỗi phase/sub-agent phải có danh sách file "owned"
- 1 file chỉ thuộc 1 phase
- Nếu cần file shared → phải chuyển task về tuần tự

## Phase template

```markdown
## Phase X
- Owner: agent-name
- Files owned:
  - path/a
  - path/b
- Dependencies:
  - phase Y (optional)
- Deliverable:
  - ...
```

## File ownership matrix (bắt buộc với task song song)

```markdown
| File | Phase | Owner |
|------|-------|-------|
| skills/example-skill/SKILL.md | Phase-1 | subagent-A |
| tools/example_tool.py | Phase-2 | subagent-B |
```

## Conflict policy
- Phát hiện overlap file → stop parallel, re-split phase
- Không merge khi ownership chưa rõ

## Category
quality-ops

## Trigger

Use this skill when:
- Multi-agent parallel tasks cần tránh file conflict
- Nhiều process cùng đọc/ghi file
- User says: "tránh file conflict", "parallel file lock", "file ownership"
