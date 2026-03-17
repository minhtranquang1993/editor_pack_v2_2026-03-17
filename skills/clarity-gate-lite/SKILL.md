---
name: clarity-gate-lite
description: Evidence-first completion gate for important outputs. Use before marking tasks done (especially publish/report/code) to verify acceptance criteria, proof, risks, and next actions.
---

# Clarity Gate Lite

Mục tiêu: không báo "xong" nếu chưa đủ bằng chứng.

## Khi bật gate
- Output quan trọng: publish, gửi KH, report, code/config thay đổi
- Task có acceptance criteria cụ thể

## Gate checklist (bắt buộc)

1. **Acceptance fit**
   - Output có đủ các mục user yêu cầu chưa?

2. **Evidence**
   - Có bằng chứng kiểm tra (test log / file diff / link output) chưa?

3. **Risk note**
   - Còn rủi ro tồn đọng nào không? (nếu có phải nêu rõ)

4. **Next action**
   - Bước tiếp theo đề xuất là gì?

## Output format

```text
🧪 Clarity Gate
- Acceptance: PASS|FAIL
- Evidence: PASS|FAIL (kèm 1-2 dòng chứng minh)
- Risk: NONE|LOW|MEDIUM|HIGH
- Next: ...
- Verdict: READY|NOT_READY
```

## Rule
- Nếu Acceptance hoặc Evidence FAIL => Verdict = NOT_READY
- Không được dùng ngôn ngữ mơ hồ kiểu "chắc ổn".

## Category
quality-ops

## Trigger

Use this skill when:
- Trước khi publish, deploy, hoặc send output
- Cần review chất lượng trước khi hoàn thành
- User says: "kiểm tra trước khi xong", "review trước khi deploy", "clarity check"
