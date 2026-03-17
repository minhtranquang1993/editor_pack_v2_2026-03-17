---
name: plan-validation-lite
description: Short validation interview before executing complex plans. Use when task is high-impact, has unclear assumptions, or involves multiple steps; ask 3-6 targeted questions on assumptions, risks, tradeoffs, and scope.
---

# Plan Validation Lite

Mục tiêu: giảm làm sai hướng trước khi execute task lớn.

## Trigger
- Task > 3 bước
- Task có risk cao (publish/deploy/send KH)
- Yêu cầu còn mơ hồ

## Cách chạy

Hỏi nhanh 3-6 câu, ưu tiên 4 nhóm:
1. Assumptions
2. Risks
3. Tradeoffs
4. Scope boundary

## Question bank (dùng chọn lọc)

- Mục tiêu chính của task này là gì (1 KPI duy nhất)?
- Cái gì KHÔNG nằm trong scope lần này?
- Rủi ro lớn nhất nếu làm sai là gì?
- Nếu phải đánh đổi, ưu tiên tốc độ hay độ chắc chắn?
- Deadline “usable” sớm nhất là khi nào?
- Điều kiện để anh gọi là “done” cụ thể là gì?

## Output format

```text
✅ Plan Validation
- Goal/KPI: ...
- In-scope: ...
- Out-of-scope: ...
- Main risk: ...
- Tradeoff chosen: ...
- Definition of done: ...
```

## Category
quality-ops
