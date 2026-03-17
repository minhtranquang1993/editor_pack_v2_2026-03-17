---
name: context-warning
description: Estimate context load and trigger warnings/compression at thresholds (60/70/80/90%). Use in long sessions to avoid sudden context overflow and preserve key decisions.
---

# 📋 SKILL: Context Warning (80% threshold)
# Location: /root/.openclaw/workspace/skills/context-warning/

## Mô tả
Ước tính token đang dùng, cảnh báo trước khi bị auto-compact.
Tránh mất context bất ngờ.

---

## Token Estimation Heuristic

```
Ước tính thô (không cần đếm chính xác):

messages_count    × 150 tokens/message  (average)
+ code_blocks     × 400 tokens/block
+ long_outputs    × 500 tokens/output   (khi em trả lời dài)
+ file_reads      × 300 tokens/file     (khi em đọc file)

total_estimate = sum of above
```

### Warning thresholds:
| Level | Estimate | Hành động |
|-------|----------|-----------|
| 🟢 Safe | < 60% | Bình thường |
| 🟡 Warning | 60-70% | Internal note (im lặng) |
| 🟠 Compress | 70-80% | **Auto-compress**: tóm tắt conversation cũ, giữ decisions + next steps |
| 🔴 Critical | > 80% | Cảnh báo + emergency save |
| ☠️ Danger | > 90% | Cảnh báo mạnh + suggest /new |

---

## Auto-Compress (70-80%) — Anchored Iterative Summary

Khi context đạt 70-80%, em tự nén bằng cách tạo summary thay thế conversation cũ.
Tham chiếu pattern chuẩn tại: `references/anchored-iterative-summary.md`

```markdown
## Session Summary (auto-compressed)

### Session Intent
[Mục tiêu ban đầu của session]

### Decisions Made
- [Quyết định 1 + lý do]
- [Quyết định 2 + lý do]

### Files Modified
- [file.py: thay đổi gì]

### Current State
[Đang ở bước nào]

### Next Steps
1. [Việc cần làm tiếp]
```

**Quan trọng:** Merge content mới vào summary hiện có, KHÔNG regenerate toàn bộ.
**Giữ lại:** Decisions, files modified, current state, next steps.
**Bỏ:** Chit-chat, output đã xử lý xong, intermediate research.

---

## Context Budget (Sonnet ~200K tokens)

```
Total: ~200,000 tokens
├── System prompt + workspace files: ~20,000 (fixed, mỗi session)
├── Conversation history: remaining budget
└── Safe cutoff: ~160,000 (80%)
```

---

## Monitoring

Em track trong session:
```json
{
  "context_monitor": {
    "message_count": 0,
    "estimated_tokens": 0,
    "last_checked_at": "",
    "warning_sent": false
  }
}
```

Cập nhật sau mỗi ~10 tin nhắn.

---

## Cảnh báo khi > 80%

```
⚠️ Context sắp đầy (~80% đã dùng)!

Em đã auto-save session rồi.

Anh nên:
1. Gõ /new để bắt đầu session mới (sạch hơn)
2. Trong session mới, gõ /recap để load lại context
3. Tiếp tục làm việc bình thường

💾 Đã lưu: {summary} vào memory/snapshots/
```

---

## Emergency Save khi > 80%

Khi detect critical threshold:
1. Trigger `auto-save` skill → save snapshot
2. Update `memory/handover.md`
3. Hiển thị cảnh báo cho anh
4. Tiếp tục hoạt động bình thường (không force stop)

---

## Tại sao không đếm chính xác?

Em không có API để đếm token chính xác.
Heuristic đủ tốt vì:
- Mục tiêu là cảnh báo SỚM, không cần chính xác tuyệt đối
- Thà cảnh báo sớm hơn là bị compact bất ngờ
- Nếu estimate sai → anh vẫn còn context để làm việc

---

## Integration

- **Auto-save:** Trigger emergency save khi > 80%
- **Handover:** Tạo handover.md để session mới resume dễ
- **/recap:** Session mới dùng /recap để load lại
- **Daily log:** Ghi lại context size warning vào log

## Observation Masking — Giữ context sạch

Khi tool output quá dài (>200 lines hoặc >5000 chars):

**PHẢI tóm tắt:**
- Web fetch / crawl → giữ key findings, bỏ boilerplate HTML
- File read dài → giữ sections relevant, note "xem thêm tại file X"
- API response lớn → extract data cần, bỏ metadata thừa
- Repeated output → reference lần đầu, không lặp lại

**KHÔNG được tóm tắt:**
- Output đang active reasoning (cần để suy luận tiếp)
- Most recent tool call (cần để trả lời user)
- Critical data (số liệu, credentials, config)

## Four-Bucket Decision Framework — Chọn đúng strategy

Khi context > 70%, **xác định loại content chiếm nhiều nhất** rồi chọn đúng bucket:

| Content chiếm nhiều nhất | Strategy | Cách làm |
|---|---|---|
| Tool outputs dài (API, file, fetch) | **Observation Masking** | Tóm tắt key findings, bỏ raw data |
| Docs/research cũ (đã dùng xong) | **Compress** | Summarize thành 2-3 bullet, bỏ chi tiết |
| Chat history dài (nhiều turns) | **Compact** | Anchored summary: giữ decisions + next steps |
| Task phức tạp (nhiều bước còn lại) | **Isolate** | Split sang sub-agent với clean context |

**KHÔNG "nén bừa"** — phân loại trước, chọn đúng bucket, rồi mới act.

## Category
memory-context
