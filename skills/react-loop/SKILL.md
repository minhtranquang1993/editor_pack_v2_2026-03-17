---
name: react-loop
description: >-
  ReAct (Reasoning + Acting) loop chuẩn cho em. Self-correction khi tool fail,
  max iterations limit để tránh loop vô hạn. Dùng ngầm trong mọi task phức tạp
  nhiều bước — em KHÔNG thông báo đang dùng ReAct, chỉ follow pattern.
---

# 📋 SKILL: ReAct Loop (Reasoning + Acting)
# Location: /root/.openclaw/workspace/skills/react-loop/

## Mô tả

ReAct = **Re**asoning + **Act**ing loop chuẩn.
Em follow pattern này cho mọi task phức tạp, nhiều bước, cần tool.

---

## Core Loop

```
THOUGHT → ACTION → OBSERVE → [lặp lại hoặc ANSWER]
```

### Dynamic Scope Adjustment

Mỗi iteration, em **đánh số + tự điều chỉnh scope**:
```
[ReAct 1/5] THOUGHT: Phân tích task...
[ReAct 2/5] OBSERVE: Phức tạp hơn dự kiến → adjust lên 2/8
[ReAct 3/8] THOUGHT: Cần thêm research...
[ReAct 4/8] OBSERVE: Đơn giản hơn tưởng → adjust xuống 4/6
```

**Expand:** Phát hiện phức tạp hơn → tăng total iterations
**Contract:** Đơn giản hơn dự kiến → giảm total
**Revise:** Insight mới invalidate bước trước → mark revision, quay lại

### Meta-Thinking — Detect "Circling"

Nếu thấy mình **lặp lại pattern** (thử cùng cách 2+ lần, output không thay đổi):
```
[ReAct 4/7 META] PAUSE: Em đang lặp pattern X, 2 lần thử cùng cách không tiến bộ
  → Missing: [điều em đang thiếu]
  → Adjust: [đổi strategy / hỏi anh / dừng lại]
```
- 2 lần retry cùng cách → BẮT BUỘC dừng, hỏi "em đang miss gì?"
- Không retry lần 3 cùng approach — đổi hướng hoặc báo anh

### Chi tiết từng bước:

**THOUGHT:** Em nghĩ gì cần làm tiếp, tại sao, dự kiến kết quả
**ACTION:** Gọi đúng 1 tool với params cụ thể
**OBSERVE:** Nhận kết quả, đánh giá — đúng không, cần làm gì tiếp
**ANSWER:** Khi đã đủ thông tin → trả lời final, DỪNG loop

---


## Implementation Details

Xem `references/implementation.md` cho: pseudo-code, self-correction logic, loop state tracking, output format.

## Max Iterations Config

| Task type | Max iterations |
|-----------|---------------|
| Simple (Q&A, lookup) | 3 |
| Medium (research, write) | 6 |
| Complex (pipeline, multi-step) | 10 |
| Default | 8 |

Khi đạt max iterations:
```
→ Synthesize từ những gì đã có
→ Báo anh: "Em đã làm được X/Y bước, còn thiếu [Z]"
→ KHÔNG loop tiếp vô hạn
```

---

## Khi nào dùng ReAct

**Tự động dùng khi:**
- Task cần nhiều tool calls (> 1 tool)
- Task cần research rồi mới viết
- Task có dependency (làm A xong mới làm được B)
- Có thể fail → cần retry logic

**Không cần khi:**
- Task 1 bước đơn giản ("thời tiết hôm nay?")
- Câu hỏi kiến thức không cần tool
- Small talk

---

## Category
automation

## Trigger

Use this skill when:
- Task phức tạp cần self-correction loop
- Multi-step task với khả năng tự sửa lỗi
- User says: "react loop", "self-correction", "chạy lại nếu sai", "auto-fix loop"