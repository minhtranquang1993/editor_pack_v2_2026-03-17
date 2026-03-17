---
name: progress-tracker
description: Track multi-step project progress with phases, completed counts, and concise status views. Use when tasks span many steps/sessions and progress visibility is required.
---

# 📋 SKILL: Progress Tracking
# Location: /root/.openclaw/workspace/skills/progress-tracker/

## Mô tả
Track tiến độ task nhiều bước, hiển thị % hoàn thành.
Dùng cho các task lớn: SEO content series, automation projects, etc.

---

## Khi nào dùng
- Task có nhiều bước / phases rõ ràng
- Anh muốn biết đã làm được bao nhiêu
- Project kéo dài nhiều ngày

---

## Session Schema (Mở rộng từ session.json)

```json
{
  "active_project": {
    "name": "SEO Articles - Thành Hưng",
    "total_tasks": 10,
    "completed_tasks": 3,
    "phases": [
      {
        "name": "Research keywords",
        "status": "completed",
        "tasks_done": 1,
        "tasks_total": 1
      },
      {
        "name": "Write articles",
        "status": "in_progress",
        "tasks_done": 2,
        "tasks_total": 8
      },
      {
        "name": "QA & Publish",
        "status": "pending",
        "tasks_done": 0,
        "tasks_total": 1
      }
    ]
  }
}
```

---

## Progress Display Format

### Khi anh hỏi tiến độ / `/next` / `/recap`:
```
📊 TIẾN ĐỘ: SEO Articles - Thành Hưng

████████░░░░░░░░░░░░ 30% (3/10 tasks)

Phase 1 - Research:    ✅ Done
Phase 2 - Writing:     🟡 2/8 articles
Phase 3 - QA/Publish:  ⬜ Chưa bắt đầu

📍 Đang làm: Bài #3 — "vận chuyển văn phòng HCM"
⏭️ Tiếp theo: Viết bài #4
```

### Progress bar logic:
```
filled = round(percent / 5)  # 20 chars total
bar = "█" * filled + "░" * (20 - filled)
```

---

## Auto-update Progress

Em tự update khi:
- Anh confirm xong một task → `tasks_done += 1`
- Em hoàn thành một bước → update `status`
- Session end → save vào `session.json`

---

## Tích hợp với các skills khác

**Auto-save:** Save progress sau mỗi task complete
**`/next`:** Hiển thị progress bar khi có active_project
**`/recap`:** Level 2 trở lên hiển thị progress
**Decision extractor:** Ghi lại milestone decisions

---

## Ví dụ thực tế với anh

```
Task: "Viết 10 bài SEO cho Thành Hưng"

Em tạo project:
  name: "SEO - Thành Hưng Q1"
  phases:
    - Research: 1 task
    - Writing: 10 articles
    - Review: 1 task
  total: 12 tasks

Mỗi bài viết xong:
  → tasks_done += 1
  → progress = tasks_done / total * 100
  → Save to session.json
  → Report: "Xong bài 3/10 ✅ (25%)"
```

## Category
quality-ops

## Trigger

Use this skill when:
- Multi-step project cần track phần trăm hoàn thành
- Cần hiển thị progress bar cho task dài
- User says: "track progress", "tiến độ bao nhiêu %", "progress report"