---
name: auto-save
description: Auto-save and handover session context on leave/decision/task-complete signals. Use when continuity is required across sessions to avoid losing decisions, pending tasks, and progress.
---

# 📋 SKILL: Auto-Save & Handover
# Location: /root/.openclaw/workspace/skills/auto-save/

## Mô tả
Tự động lưu session context để không bao giờ mất context.
Chạy ngầm, không cần anh nhắc.

## Session state chuẩn
- Dùng file chuẩn: `memory/session_state.json`
- Schema tham chiếu: `config/session-state.schema.json`

---

## Trigger Conditions

### 1. User leaving — detect patterns trong tin nhắn:
```
patterns = [
  "bye", "tạm biệt", "tạm nghỉ", "tam biet", "tam nghi",
  "tối đi", "đi ăn", "đi ngủ", "mai làm tiếp", "hôm nay xong rồi",
  "hết giờ", "save lại", "đóng app", "tắt máy",
  "thôi nhé", "oke em nhé", "ok nghỉ"
]
→ trigger = "user_leaving" → Full save + thông báo
```

### 2. Decision detected — detect patterns:
```
patterns = [
  "ok làm vậy", "chọn cái này", "dùng cái này", "đồng ý",
  "quyết định là", "mình sẽ dùng", "ok anh chọn", "oke theo",
  "thống nhất", "confirm"
]
→ trigger = "decision_made" → Silent save + log decision
```

### 3. Task completed — detect patterns:
```
patterns = [
  "xong rồi", "done", "hoàn thành", "ok xong", "✅",
  "đã xong", "implement xong", "deploy xong"
]
→ trigger = "task_complete" → Save + update progress
```

### 4. Periodic checkpoint:
```
Mỗi 15 tin nhắn trong session → Silent save
```

### 5. Context warning (80% threshold — xem Step 11):
```
Khi context > 80% → Emergency save + cảnh báo
```

### 6. Anchored summary sync:
```
Khi context-warning tạo bản AIS mới → auto-save cập nhật session_state
và ghi checkpoint để /recap resume đúng anchor.
```

---

## Execution Logic

### Khi trigger kích hoạt:

**Bước 1:** Cập nhật `memory/session_state.json`:
```json
{
  "summary": {
    "current_feature": "[task đang làm]",
    "current_task": "[task cụ thể]",
    "status": "in_progress | completed | blocked",
    "progress_percent": 0-100,
    "last_action": "[hành động cuối]",
    "next_step": "[gợi ý bước tiếp]"
  },
  "updated_at": "[ISO timestamp]",
  "message_count": N
}
```

**Bước 2:** Append vào `memory/session_log.txt`:
```
[TIMESTAMP] [TRIGGER] [SUMMARY 1 dòng]
```

**Bước 3:** Nếu trigger = `user_leaving`:
- Tạo `memory/handover.md` (xem format bên dưới)
- Snapshot vào `memory/snapshots/YYYY-MM-DD_HHMM.json`
- Thông báo: "💾 Đã lưu session. Mai mở lại gõ /recap là nhớ hết nha anh!"

**Bước 4:** Nếu trigger = `decision_made`:
- Append vào `session_state.json` → `decisions_made`
- Silent (không thông báo)

**Bước 5:** Nếu trigger = `task_complete`:
- Update `progress_percent`
- Append vào `recent_changes`
- Thông báo: "💾 Đã lưu tiến độ."

**Sub-step 5a — Update working-context.md:**
- Đọc `memory/working-context.md`
- Trong section "Active Tasks": mark task vừa done với ✅ + timestamp:
  ```
  - {YYYY-MM-DD}: ✅ {summary.current_task} — done
  ```
- Nếu `summary.next_step` có giá trị → thêm dòng mới:
  ```
  - ⏳ Next: {summary.next_step}
  ```
- Trong section "Recent Context": append 1 dòng:
  ```
  - {YYYY-MM-DD}: {summary.current_feature} → completed
  ```
- Silent (không thông báo)

**Sub-step 5b — Trigger quality drift log:**
```bash
python3 tools/quality_drift_detector.py --log-session
```
- Silent, chạy ngầm sau khi update working-context
- Non-blocking: nếu fail thì bỏ qua, không ảnh hưởng flow chính

---

## Handover Format (`memory/handover.md`)

```markdown
# 🤝 Handover — {DATE} {TIME}

## Đang làm gì
{summary.current_feature} → {summary.current_task}
Status: {status} ({progress}%)

## Quyết định gần đây
{decisions_made[-3:]}

## Việc chưa xong
{pending_tasks[:5]}

## Bước tiếp theo
{next_step}

## Ghi chú
{any important notes}
```

---

## Snapshot Management

- Save: `memory/snapshots/YYYY-MM-DD_HHMM.json`
- TTL: **7 ngày** → xóa snapshot cũ hơn 7 ngày tự động
- Restore: Nếu `session_state.json` bị lỗi → load snapshot mới nhất

---

## Thông báo cho anh

| Trigger | Thông báo |
|---------|-----------|
| user_leaving | "💾 Đã auto-save. Mai gõ /recap để tiếp tục nha anh!" |
| task_complete | "💾 Đã lưu tiến độ." |
| periodic | (im lặng) |
| decision_made | (im lặng) |
| emergency | "⚠️ Context sắp đầy! Đã save backup. Nên /new session rồi /recap." |

---

## Khi session mới bắt đầu

1. Check `memory/handover.md` tồn tại không?
   - Có → Đọc → Hiển thị summary → Hỏi "Tiếp tục từ đây không anh?"
   - Sau khi confirm → Xóa handover.md
2. Không có → Load `session_state.json` level 1 (silent, auto-inject vào context)

## Category
memory-context
