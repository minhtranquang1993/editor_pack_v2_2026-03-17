---
name: next
description: Recommend the most relevant next step from current session state, pending items, and blockers. Use when user asks /next or needs immediate direction.
---

# 📋 SKILL: /next — The Compass
# Location: /root/.openclaw/workspace/skills/next/

## Mô tả
Gợi ý bước tiếp theo dựa trên context hiện tại.
Khi anh không biết làm gì tiếp, gõ /next.

---

## Trigger
- Anh gõ `/next`
- Anh nói "làm gì tiếp", "tiếp theo là gì", "bây giờ làm gì"

---

## Execution Logic

### Bước 1: Đọc context

```
Load memory/session_state.json → summary, pending_tasks, status, errors
```

### Bước 2: Xác định trạng thái

| Trạng thái | Dấu hiệu | Gợi ý |
|-----------|----------|-------|
| Không có task | session trống | Hỏi anh muốn làm gì |
| Có task đang dở | status = in_progress | Tiếp tục task đó |
| Task vừa xong | status = completed | Suggest task tiếp trong pending |
| Bị blocked | status = blocked | Debug / hỏi thêm info |
| Có lỗi chưa fix | errors_encountered | Fix lỗi trước |
| Pending > 3 | pending_tasks nhiều | Suggest theo priority |

### Bước 3: Output format

```
🧭 ĐANG Ở ĐÂU:
[Mô tả ngắn tình trạng hiện tại]

➡️ LÀM GÌ TIẾP:
1. [Gợi ý cụ thể nhất]
2. [Gợi ý thay thế]
3. [Gợi ý optional]

💡 MẸO: [Lời khuyên nếu có]
```

---

## Templates theo trạng thái

### Không có task / session trống:
```
🧭 Đang ở đây: Chưa có task active.

➡️ Làm gì tiếp:
1. Kể cho em nghe anh muốn làm gì?
2. Xem lại MEMORY.md để nhớ project cũ
3. Bắt đầu task mới

💡 Mẹo: Anh hay làm SEO content — muốn viết bài mới không?
```

### Có task đang dở:
```
🧭 Đang làm: {current_feature} → {current_task} ({progress}%)

➡️ Làm gì tiếp:
1. Tiếp tục: {next_step}
2. Review lại: /recap full để xem tổng thể
3. Đổi task: Gõ tên task mới

💡 {pending_tasks.length} việc khác đang chờ.
```

### Task vừa hoàn thành:
```
🧭 Vừa xong: {last_completed_task} ✅

➡️ Làm gì tiếp:
1. [Task tiếp theo trong pending với priority cao nhất]
2. Review output vừa làm
3. Nghỉ ngơi 😄

💡 Tốt lắm anh! {progress}% tổng tiến độ.
```

### Có lỗi chưa fix:
```
🧭 Đang có vấn đề: {error_count} lỗi chưa resolve.

➡️ Làm gì tiếp:
1. Fix lỗi: {errors[0].description}
2. Bỏ qua + làm task khác
3. Mô tả lỗi cho em để debug

💡 Lỗi: "{errors[0].message}" — em có thể giúp!
```

### Nhiều pending tasks:
```
🧭 Queue của anh: {pending_tasks.length} tasks đang chờ.

➡️ Priority cao nhất:
1. 🔴 [HIGH] {pending[0]}
2. 🟡 [MED] {pending[1]}
3. 🟢 [LOW] {pending[2]}

💡 Làm cái nào trước anh?
```

---

## Fallback
```
Nếu không có session_state.json:
→ "Em chưa có context. Anh đang làm gì? Kể cho em nghe nhé!"
```

## Category
quality-ops
