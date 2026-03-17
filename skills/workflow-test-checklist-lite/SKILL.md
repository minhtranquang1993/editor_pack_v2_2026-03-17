---
name: workflow-test-checklist-lite
description: Step-by-step workflow validation with Pass/Fail/Skip checkpoints. Use when testing end-to-end business workflows (content, ads, email, reporting) before rollout.
---

# Workflow Test Checklist Lite

Mục tiêu: test workflow nghiệp vụ theo checklist rõ ràng.

## Checklist format

```markdown
# Workflow Test: {name}

## Step 1 - ...
- Action: ...
- Expected: ...
- Result: PASS | FAIL | SKIP
- Note: ...

## Step 2 - ...
...

## Summary
- Pass: X
- Fail: Y
- Skip: Z
- Verdict: READY | NOT READY
```

## Rules
- Mỗi step phải có expected outcome trước khi chạy
- Fail ở step critical → verdict NOT READY
- Không bỏ qua fail nếu chưa có mitigation rõ

## Suggested critical workflows
- yt-content (transcript → content)
- report-ads (fetch → calc → output)
- blog publish (draft → SEO meta → publish)

## Category
quality-ops

## Trigger

Use this skill when:
- Cần test workflow end-to-end trước khi rollout
- Tạo checklist kiểm tra trước khi triển khai
- User says: "test workflow", "checklist trước khi rollout", "workflow checklist"