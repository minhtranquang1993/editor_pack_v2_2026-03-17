---
name: context-help
description: Provide context-aware help based on current session state (no-task/working/blocked/completed). Use when user asks /help, feels stuck, or asks what to do next within active workflow.
---

# 📋 SKILL: Context Help
# Location: /root/.openclaw/workspace/skills/context-help/

## Mô tả
Trả lời /help hoặc câu hỏi dựa trên trạng thái hiện tại của anh.
Thay vì help chung chung → help đúng với anh đang làm gì.

---

## Trigger
- Anh gõ `/help`
- Anh nói "giúp em với", "làm sao", "không hiểu", "bị kẹt"
- Anh hỏi "?" một mình

---

## Execution

### Bước 1: Đọc context
```
Load memory/session_state.json → status, current_feature, current_task, pending
```

### Bước 2: Detect trạng thái

| State | Dấu hiệu |
|-------|----------|
| `no_task` | session trống hoặc không có |
| `working` | status = in_progress |
| `stuck` | status = blocked hoặc errors chưa fix |
| `completed` | status = completed |
| `idle` | Không có task active |

### Bước 3: Trả lời theo context

---

## Help Templates

### `no_task` — Chưa có task
```
👋 Em có thể giúp gì cho anh?

Anh muốn:
1. 🔍 Research thông tin → Kể cho em chủ đề
2. ✍️ Viết content/SEO → Cho em biết keyword
3. 🤖 Automation/code → Mô tả vấn đề
4. 📊 Phân tích dữ liệu → Share file/data
5. 🌦️ Thời tiết/tin tức → Hỏi thẳng đi anh

💡 Hoặc gõ /next nếu muốn em gợi ý.
```

### `working` — Đang làm task
```
💡 Anh đang làm: {current_feature}
   └─ Task: {current_task} ({progress}%)

Em có thể giúp:
1. Tiếp tục task này
2. Giải thích bước nào đó
3. Xem lại kết quả
4. Đổi sang task khác

Anh cần gì cụ thể?
```

### `stuck` — Bị kẹt / blocked
```
😅 Có vẻ đang bị kẹt ở: {current_task}

Thử nhé:
1. Mô tả cụ thể vấn đề cho em nghe
2. /recap full — xem lại toàn bộ context
3. Đổi task khác trong pending, quay lại sau
4. Em debug cùng — paste lỗi hoặc mô tả

💡 {pending_tasks.length} task khác đang chờ nếu muốn switch.
```

### `completed` — Vừa xong task
```
✅ Vừa xong: {last_task}

Làm gì tiếp?
1. /next — Em gợi ý task tiếp theo
2. Review output vừa làm
3. Start task mới — kể cho em nghe

🎉 Anh đã {progress}% tổng tiến độ!
```

### `idle` — General help
```
👋 Alo anh! Em đây.

Lệnh hay dùng:
• /next      → Gợi ý việc tiếp theo
• /recap     → Nhớ lại context
• /recap full → Xem chi tiết hơn

Skills em có:
• Search web, research thông tin
• Viết SEO content
• Automation / code
• Phân tích dữ liệu
• Thời tiết, tin tức

Hoặc anh cứ nói thẳng muốn làm gì! 😊
```

---

## Fallback
Nếu không có session_state.json → dùng template `idle`.

## Response Template Pack (Tier-3)

```text
🧭 Trạng thái hiện tại: ...
✅ Nên làm ngay: ...
⏭️ Bước sau đó: ...
```

## Definition of Done (Tier-3)
- User biết ngay phải làm gì tiếp theo trong 1-2 bước.

## Category
quality-ops
