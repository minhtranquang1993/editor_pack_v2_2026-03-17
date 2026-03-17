---
name: test-orchestrator-lite
description: Practical test gate for code or automation changes. Use when modifying scripts/config/workflows to ensure compile/lint/smoke checks run before marking task done, with a concise pass/fail summary.
---

# Test Orchestrator Lite

Mục tiêu: không báo "xong" trước khi verify.

## Default policy
- Đọc policy tại `references/default-test-gate-policy.md` trước khi áp dụng gate.
- Mặc định: task có sửa code/script/config/workflow => bắt buộc test gate.

## Test gate (minimum)

Sau khi sửa code/script/config, chạy theo thứ tự:

1. **Syntax/compile check**
   - Python: `python3 -m py_compile <file_or_files>`
   - JS/TS: dùng lệnh build/typecheck phù hợp repo

2. **Target smoke test**
   - Chạy command nhỏ nhất để xác nhận chức năng vừa sửa hoạt động

3. **Regression quick check**
   - Đảm bảo thay đổi mới không làm hỏng luồng liên quan trực tiếp

## Pass/Fail rule

- Có bước fail → chưa được chốt done
- Fix xong phải re-run bước fail
- Chỉ chốt done khi toàn bộ gate pass

## Report format

```text
✅ Test Gate
- Syntax/compile: PASS|FAIL
- Smoke test: PASS|FAIL
- Regression quick check: PASS|FAIL
- Evidence: [1-2 dòng output quan trọng]
```

## With Clarity Gate
- Sau khi test gate PASS, chạy `clarity-gate-lite` để ra verdict cuối: READY/NOT_READY.

## Anti-fake rule

- Không dùng fake success message
- Không bỏ qua test fail để "cho xong"
- Nếu thiếu môi trường test, nêu rõ phần nào chưa verify được

## Category
quality-ops

## Trigger

Use this skill when:
- Sau khi sửa script/config cần test trước khi deploy
- Cần orchestrate nhiều test cases
- User says: "test trước khi deploy", "run tests", "test orchestrator"