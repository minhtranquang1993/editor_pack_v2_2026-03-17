---
name: notify-on-complete-lite
description: Lightweight completion notification pattern for long-running tasks and sub-agents. Use when execution is asynchronous or takes long enough that user should be alerted on completion with concise summary.
---

# Notify on Complete Lite

Mục tiêu: task dài xong là báo anh ngay, không spam.

## Khi dùng
- Task nền / task dài > 10 phút
- Có sub-agent chạy độc lập
- Có cron/job hoàn thành cần update

## Message format

```text
🔔 Task xong: {task-name}
- Kết quả: ✅/❌
- Output chính: ...
- Next đề xuất: ...
```

## Anti-spam
- Cooldown 10 phút cho cùng 1 loại event
- Không gửi notify cho task nhỏ < 2 phút

## Nếu fail

```text
⚠️ Task lỗi: {task-name}
- Lý do chính: ...
- Em đã thử: ...
- Cần anh quyết: ...
```

## Category
quality-ops

## Trigger

Use this skill when:
- Long-running async task cần thông báo khi hoàn thành
- Cần alert qua Telegram/email khi task xong
- User says: "báo khi xong", "notify when done", "alert khi hoàn thành"
