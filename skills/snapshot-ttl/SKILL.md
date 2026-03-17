---
name: snapshot-ttl
description: Manage session snapshots and TTL cleanup to keep recoverability without workspace clutter. Use for periodic state capture and safe pruning of stale snapshots.
---

# 📋 SKILL: Snapshot & TTL Management
# Location: /root/.openclaw/workspace/skills/snapshot-ttl/

## Mô tả
Quản lý snapshot + tự động xóa file cũ để workspace gọn gàng.

---

## Snapshot

### Khi nào tạo snapshot:
1. Anh leave session (detect "bye", "tạm nghỉ"...)
2. Task lớn hoàn thành (status = completed)
3. Mỗi ngày cuối ngày (nếu có hoạt động)

### Format file:
```
memory/snapshots/YYYY-MM-DD_HHMM.json
```

### Nội dung snapshot:
```json
{
  "created_at": "2026-02-20T19:30:00Z",
  "trigger": "user_leaving | task_complete | daily",
  "session_summary": {
    "project": "...",
    "feature": "...",
    "task": "...",
    "status": "...",
    "progress": 0
  },
  "decisions_made": [...],
  "pending_tasks": [...],
  "recent_changes": [...]
}
```

---

## TTL Rules

| File type | TTL | Lý do |
|-----------|-----|-------|
| `memory/snapshots/*.json` | **7 ngày** | Backup ngắn hạn |
| `memory/YYYY-MM-DD.md` (daily logs) | **30 ngày** | Warm context |
| `memory/session.json` | Không xóa | Current state |
| `memory/handover.md` | Xóa sau khi resume | One-time use |
| `MEMORY.md` | Không xóa | Long-term memory |

---

## Cleanup Logic

Em tự chạy cleanup khi:
- Session start (check trước khi làm việc)
- Hoặc khi anh gọi `/recap` (check ngầm)

```python
# Pseudo-code
def cleanup_snapshots():
    cutoff = now() - 7_days
    for file in memory/snapshots/:
        if file.created_at < cutoff:
            delete(file)

def cleanup_daily_logs():
    cutoff = now() - 30_days
    for file in memory/*.md:
        if file.date < cutoff:
            delete(file)
```

---

## Restore từ Snapshot

Khi `session.json` bị lỗi hoặc mất:
1. Tìm snapshot mới nhất trong `memory/snapshots/`
2. Load và restore `session.json` từ đó
3. Thông báo: "Đã khôi phục từ backup {date}. Tiếp tục nhé anh!"

---

## Disk Usage Estimate
- Mỗi snapshot: ~2-5KB
- 7 ngày × 2 snapshots/ngày = ~14 files × 5KB = ~70KB
- Daily logs: ~5KB/ngày × 30 ngày = ~150KB
- Total: < 1MB — không đáng kể

---

## Implementation Notes

Khi implement cleanup, em dùng:
```bash
# List snapshots older than 7 days
find /root/.openclaw/workspace/memory/snapshots/ -name "*.json" -mtime +7

# Delete them
find /root/.openclaw/workspace/memory/snapshots/ -name "*.json" -mtime +7 -delete

# List daily logs older than 30 days
find /root/.openclaw/workspace/memory/ -name "20[0-9][0-9]-*.md" -mtime +30
```

## Category
memory-context
