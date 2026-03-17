---
name: aot-executor
description: >-
  AoT Executor — nhận JSON plan từ aot-planner, chạy atoms theo dependency
  order, manage state, retry khi fail, QA loop khi codex trả FAIL.
  Kết hợp với aot-planner để tạo thành full pipeline.
---

# 📋 SKILL: AoT Executor
# Location: /root/.openclaw/workspace/skills/aot-executor/

## Mô tả

Nhận plan JSON từ `aot-planner` → execute atoms theo đúng dependency order.
Quản lý state, retry logic, và self-correction loop khi QA fail.

---

## Execution Flow

```
JSON Plan
    │
    ▼
┌─────────────────────────────────┐
│  1. Topological Sort            │
│     (dependency order)          │
└─────────────┬───────────────────┘
              │
    ┌─────────▼─────────┐
    │  For each atom:   │
    │                   │
    │  ✓ Deps done?     │
    │  ✓ Resolve refs   │
    │  ✓ Spawn agent    │
    │  ✓ Store result   │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  If QA atom FAIL: │
    │  → Trigger fix    │
    │  → Re-run writer  │
    │  → Re-run QA      │
    │  (max 2 retries)  │
    └─────────┬─────────┘
              │
    ┌─────────▼─────────┐
    │  Final atom:      │
    │  Collect results  │
    │  Report to anh    │
    └───────────────────┘
```

---

## State Management

```json
{
  "plan_id": "plan_20260220_001",
  "task": "SEO article - vận chuyển văn phòng HCM",
  "status": "in_progress",
  "atoms_total": 6,
  "atoms_done": 0,
  "state": {
    "1": {"status": "completed", "result": "...competitor data...", "output_key": "serp_data"},
    "2": {"status": "completed", "result": "...keyword data...", "output_key": "keyword_data"},
    "3": {"status": "running"},
    "4": {"status": "pending"},
    "5": {"status": "pending"},
    "6": {"status": "pending"}
  },
  "errors": [],
  "retries": {}
}
```

---

## Progress Reporting cho anh

Sau mỗi atom hoàn thành → update session.json + optional notification:

```
[Atom 1/6] ✅ Research SERP xong
[Atom 2/6] ✅ Research Keywords xong
[Atom 3/6] ✅ Content Brief xong
[Atom 4/6] ✅ Article Draft xong (2340 từ)
[Atom 5/6] ⚠️ QA FAIL — fixing (retry 1/2)
[Atom 5/6] ✅ QA PASS sau retry 1
[Atom 6/6] ✅ Final output collected
```

---

## Full AoT Pipeline (Planner + Executor)

```
Anh: "Viết bài SEO về [keyword]"
    │
    ▼
Em (MAIN/sonnet): Nhận task, assess → cần AoT pipeline
    │
    ├─ Spawn Opus (aot-planner): generate JSON plan
    │      ↓ plan.json
    ├─ Validate plan
    │      ↓ validated
    ├─ AoT Executor:
    │    ├─ Atom 1+2 (haiku×2, parallel): Research
    │    ├─ Atom 3 (sonnet): Brief
    │    ├─ Atom 4 (sonnet): Write
    │    ├─ Atom 5 (codex): QA → [correction loop if fail]
    │    └─ Atom 6 (final): Collect
    │
    └─ Deliver to anh: article + QA report + GitHub link
```

---


## Implementation Details

Xem `references/implementation.md` cho: Executor pseudo-code, Resolve References, QA Correction Loop, Topological Sort, Parallel Execution.

## Error Handling

| Error | Hành động |
|-------|-----------|
| Atom timeout | Retry 1 lần, nếu vẫn fail → skip + note |
| Atom crash | Log error, try alternative nếu có |
| QA fail 2× | Deliver với warning: "QA không pass, anh review thêm nha" |
| Plan invalid | Re-plan với Opus (max 2 tries) |
| Missing deps | Abort + báo anh atom nào bị block |

---

## Integration với content-factory

`content-factory` skill → dùng `aot-planner` + `aot-executor` làm backend:

```
content-factory.SKILL.md gọi:
  1. aot-planner → tạo plan cho loại content (SEO/blog/social)
  2. aot-executor → chạy plan
  3. GitHub push → deliver
```

## Category
automation
