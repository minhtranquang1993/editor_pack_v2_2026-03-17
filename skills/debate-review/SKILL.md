---
name: debate-review
description: >-
  Adversarial debate loop giữa 2 AI agents (sonnet vs codex) để review plan/code/content/decision
  trước khi output. Một agent đề xuất, agent kia phản biện với ISSUE list + VERDICT.
  Loop đến khi APPROVE hoặc stalemate. Porting ý tưởng từ codex_skill cho OpenClaw.
  Trigger: "/debate-review", "debate plan", "cho 2 AI debate", "review adversarial", 
  "phản biện plan", "2 AI ngồi review", hoặc bất kỳ task cần review chất lượng cao trước khi publish/deploy.
---

# 🥊 SKILL: Debate Review
# Location: /root/.openclaw/workspace/skills/debate-review/

## Mô tả

Thay vì chỉ có 1 agent QA review 1 chiều, skill này tổ chức **tranh luận 2 chiều** giữa:
- **Agent A (Proposer)** — `sonnet`: đề xuất plan/code/content/decision
- **Agent B (Challenger)** — `codex`: phản biện, tìm lỗ hổng, raise issues

Loop cho đến khi đạt `VERDICT: APPROVE` hoặc stalemate.

---

## 3 Modes — Input/Output Contract Rõ Ràng

| Mode | Input bắt buộc | Challenger focus | Trigger |
|------|---------------|-----------------|---------|
| `plan` | File plan hoặc danh sách steps | Missing steps, wrong order, edge cases, dependencies | "debate plan", "/debate-review mode=plan" |
| `impl` | Code diff / content đã viết | Logic errors, bugs, missing error handling, security | "debate code", "review trước khi commit" |
| `think` | Câu hỏi + proposed answer/approach | Logic gaps, missing evidence, alternative approaches | "2 AI nghĩ về...", "debate về X" |

> ⚠️ Nếu input không đúng format cho mode → em hỏi anh bổ sung trước khi spawn Challenger.

---

## Severity Classification (bắt buộc từ Challenger)

Mỗi issue phải có severity tag:
- `[CRITICAL]` — blocking, **bắt buộc fix** trước khi APPROVE
- `[MAJOR]` — quan trọng, nên fix
- `[MINOR]` — nice-to-have, có thể skip

**APPROVE chỉ khi không còn `[CRITICAL]` issues chưa được resolve.**
MAJOR/MINOR còn open → vẫn có thể APPROVE, nhưng em note lại cho anh.

---

## Output Protocol (bắt buộc)

### Challenger output format:
```
ISSUE-1: [CRITICAL|MAJOR|MINOR] [Mô tả vấn đề cụ thể]
ISSUE-2: [CRITICAL|MAJOR|MINOR] [Mô tả vấn đề cụ thể]
...
VERDICT: APPROVE | REJECT
CONFIDENCE: high | medium | low
```

### Proposer response format:
```
FIX-1: [Chấp nhận + sửa cụ thể thế nào]
REBUT-2: [Bác bỏ + lý do + evidence cụ thể]
VERIFIED-1: [Confirm issue đã được address bằng change cụ thể]
...
UPDATED: [Bản cập nhật đầy đủ sau fix]
```

> ⚠️ Mỗi FIX phải kèm `VERIFIED-N` để Challenger check lại — không APPROVE nếu thiếu verification.

---

## Workflow Chi Tiết

```
Input: [plan / code / content / câu hỏi]  +  mode
    │
    ▼
Validate input đúng mode contract? → nếu không: hỏi anh bổ sung
    │
    ▼
[Round 1]
  Agent A (sonnet): Trình bày đề xuất/context rõ ràng
        │
        ▼
  Agent B (codex): Nhận toàn bộ context
    → raise ISSUE list với severity tag
    → VERDICT: APPROVE | REJECT
        │
        ├─ VERDICT: APPROVE? → ✅ Done, báo anh
        │
        ▼
  Agent A (sonnet): Xử lý từng CRITICAL issue trước:
    - FIX + VERIFIED: Chấp nhận → update proposal
    - REBUT: Bác bỏ → giải thích + evidence
        │
        ▼
[Round 2] (nếu còn CRITICAL chưa resolved)
  Agent B (codex): Check VERIFIED items trước
    → Confirm resolved hoặc raise lại nếu verification không đủ
    → Raise ISSUE mới nếu có
    → VERDICT
        │
        ├─ VERDICT: APPROVE? → ✅ Done
        ├─ Stalemate detected? → báo anh (xem Stalemate Detection)
        │
        ▼
[Max 3 rounds] → Force end → báo anh summary
```

---

## Stalemate Detection (nâng cấp)

Stalemate khi **bất kỳ điều kiện nào** dưới đây đúng:

1. **Semantic repeat:** Issues round N+1 giống round N về ý nghĩa (> 80% similar) — không chỉ so text
2. **All-low-confidence:** Toàn bộ issues trong round N+1 đều là `CONFIDENCE: low` → uncertainty, không phải real problem
3. **Pure REBUT loop:** 2 rounds liên tiếp không có FIX nào được apply
4. **Round 3 passed:** Hard cap — kết thúc dù VERDICT vẫn REJECT

**Tie-break khi stalemate:**
- Challenger `high` vs Proposer `medium` → lean Challenger
- Cả 2 `high` → present cả 2 sides, hỏi anh quyết
- Challenger `low` → override, lean Proposer
- Còn CRITICAL open sau stalemate → **bắt buộc hỏi anh** trước khi proceed

---

## Implementation Guide

### Bước 1 — Validate input theo mode

```
mode=plan  → cần: steps/plan text (hoặc file path)
mode=impl  → cần: code/content đã viết (hoặc git diff)
mode=think → cần: câu hỏi rõ ràng + proposed answer/approach
```

### Bước 2 — Spawn Agent B (Challenger / codex)

```python
spawn(
  agent="codex",
  task=f"""
  Be concise, straight to the point. No fluff. Max 300 tokens.
  You are a strict adversarial reviewer inside an AI assistant pipeline.

  [MODE: {mode}]
  [CONTEXT: {context}]
  [PROPOSAL:
  {proposal}
  ]
  {f"[PREVIOUS_ROUNDS: {previous_rounds}]" if previous_rounds else ""}

  Find weaknesses, risks, flaws. Be specific — no vague feedback.
  Tag each issue with severity: [CRITICAL] blocking | [MAJOR] important | [MINOR] nice-to-have

  Output EXACTLY:
  ISSUE-1: [CRITICAL|MAJOR|MINOR] [specific problem]
  ISSUE-2: [CRITICAL|MAJOR|MINOR] [specific problem]
  (skip if none)
  VERDICT: APPROVE (no CRITICAL issues) | REJECT (CRITICAL issues found)
  CONFIDENCE: high | medium | low
  """
)
```

### Bước 3 — Parse Challenger output

```python
import re

issues = re.findall(r'ISSUE-(\d+):\s*\[(CRITICAL|MAJOR|MINOR)\]\s*(.+)', text)
verdict = re.search(r'VERDICT:\s*(APPROVE|REJECT)', text)
confidence = re.search(r'CONFIDENCE:\s*(high|medium|low)', text)

critical_issues = [i for i in issues if i[1] == "CRITICAL"]
if verdict.group(1) == "APPROVE" or not critical_issues:
    # Done
```

### Bước 4 — Spawn Agent A (Proposer / sonnet) xử lý issues

```python
spawn(
  agent="sonnet",
  task=f"""
  Be concise, straight to the point. Max 400 tokens.
  
  Handle EACH issue below. Prioritize CRITICAL first.
  
  ISSUES:
  {issues_text}
  
  For each issue:
  FIX-{{N}}: [accept + exact change made]
  or
  REBUT-{{N}}: [reject + specific reason + evidence]
  
  After each FIX, add:
  VERIFIED-{{N}}: [confirm exactly how the issue is addressed in UPDATED]
  
  Then:
  UPDATED: [complete updated proposal with all fixes applied]
  """
)
```

### Bước 5 — Round 2: Challenger verify + re-review

Challenger nhận: original issues + VERIFIED items + UPDATED proposal.
Challenger check `VERIFIED-N` trước → confirm hoặc reject verification.
Nếu verification đủ → không raise lại issue đó.

### Bước 6 — Stalemate / End

Nếu APPROVE → deliver `UPDATED` cho anh.
Nếu stalemate → xem `references/stalemate-guide.md`.

---

## Ví dụ Sử Dụng

### Mode: plan
```
Input: "Thêm filter dịch vụ vào biểu đồ ads
Steps: 1. Sửa SQL RPC, 2. Sửa hook, 3. Sửa UI"

→ codex: ISSUE-1: [CRITICAL] SQL RPC không handle NULL → query crash
         ISSUE-2: [MAJOR] Hook không debounce → spam API
         VERDICT: REJECT | CONFIDENCE: high

→ sonnet: FIX-1: Thêm COALESCE(p_service_filter, '')
          VERIFIED-1: UPDATED step 1 có COALESCE wrap rõ ràng
          FIX-2: Thêm useMemo + debounce 300ms
          VERIFIED-2: UPDATED step 2 có debounce hook
          UPDATED: [plan đầy đủ đã sửa]

→ codex: check VERIFIED → OK → VERDICT: APPROVE | CONFIDENCE: high
```

### Mode: think
```
Input: "Nên dùng Daytona hay chạy thẳng trên server cho ads report?"

→ codex: ISSUE-1: [CRITICAL] Server không có IPv6 → Supabase query fail
         ISSUE-2: [MINOR] Daytona cold start ~2s
         VERDICT: REJECT | CONFIDENCE: high

→ sonnet: FIX-1: IPv6 blocking → Daytona bắt buộc
          VERIFIED-1: UPDATED chọn Daytona vì IPv6 constraint
          REBUT-2: 2s cold start acceptable cho report 8h sáng
          UPDATED: Dùng Daytona sandbox, pre-warm nếu cần

→ codex: VERDICT: APPROVE | CONFIDENCE: high
```

---

## Integration với Skills Khác

```
aot-planner → [plan] → debate-review (mode=plan) → [approved] → aot-executor
seo-article → [draft] → debate-review (mode=impl) → [approved] → publish
content-factory → QA step → debate-review → chất lượng cao hơn 1-chiều
```

---

## Rules

1. **KHÔNG skip** debate nếu task quan trọng (publish/deploy/gửi KH)
2. **Validate input** trước khi spawn — đúng contract theo mode
3. **Severity tag bắt buộc** — không accept issue không có `[CRITICAL|MAJOR|MINOR]`
4. **VERIFIED bắt buộc** với mỗi FIX — không APPROVE nếu thiếu
5. **Max 3 rounds** hard cap — sau đó hỏi anh
6. **Be concise** — Challenger < 300 tokens, Proposer < 400 tokens mỗi round

---

## References

- `references/prompts.md` — System prompts chi tiết cho từng mode + role
- `references/output-format.md` — Output contract đầy đủ + parse rules + stalemate detection code
- `references/stalemate-guide.md` — Khi nào declare stalemate + tie-break + how to present

## Category
quality-ops
