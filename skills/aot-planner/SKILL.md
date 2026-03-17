---
name: aot-planner
description: >-
  Atom of Thought planner. Opus (leader) nhận task → tạo JSON plan gồm các
  "atoms" nhỏ nhất. Mỗi atom có id/kind/input/dependsOn. Plan được validate
  trước khi execute. Dùng cho complex tasks cần pipeline rõ ràng.
---

# 📋 SKILL: AoT Plan Generator
# Location: /root/.openclaw/workspace/skills/aot-planner/

## Mô tả

**AoT = "SQL for Reasoning"** — tách task thành atoms nhỏ nhất, có dependency rõ ràng.

Opus (leader) tạo JSON plan → Validate → AoT Executor chạy atoms.

---

## Atom Schema

```json
{
  "id": 1,
  "kind": "research | write | qa | transform | search | fetch | decision | final",
  "agent": "haiku | sonnet | codex | tool",
  "name": "mô tả ngắn atom này làm gì",
  "input": {
    "prompt": "instruction cụ thể cho agent",
    "data": "<result_of_N>",
    "params": {}
  },
  "dependsOn": [0],
  "output_key": "research_result"
}
```

### Kinds:

| Kind | Agent | Mô tả |
|------|-------|-------|
| `research` | haiku | Search web, gather data |
| `fetch` | tool | web_fetch URL cụ thể |
| `write` | sonnet | Viết content từ brief |
| `qa` | codex | Review, validate, check |
| `transform` | haiku/sonnet | Tóm tắt, format, convert |
| `decision` | sonnet | Đưa ra decision dựa trên data |
| `final` | - | Collect kết quả, không execute |

---


## Prompt & Examples

Xem `references/prompt-examples.md` cho: Plan Generator Prompt (Opus), Ví dụ SEO Article Plan.

## Plan Validation Rules

Trước khi execute, validate plan:

```python
def validate_plan(plan):
    atom_ids = set()

    for atom in plan["atoms"]:
        # 1. ID unique
        assert atom["id"] not in atom_ids, f"Duplicate ID: {atom['id']}"
        atom_ids.add(atom["id"])

        # 2. Kind valid
        valid_kinds = ["research", "write", "qa", "transform", "fetch", "decision", "final"]
        assert atom["kind"] in valid_kinds, f"Unknown kind: {atom['kind']}"

        # 3. Agent valid
        valid_agents = ["haiku", "sonnet", "codex", "tool", None]
        assert atom["agent"] in valid_agents, f"Unknown agent: {atom['agent']}"

        # 4. Dependencies exist
        for dep_id in atom.get("dependsOn", []):
            assert dep_id in atom_ids or dep_id < atom["id"], f"Unknown dependency: {dep_id}"

        # 5. Final atom không có agent
        if atom["kind"] == "final":
            assert atom["agent"] is None, "Final atom should have agent=null"

    return True
```

---

## Self-Healing Plan

Nếu validation fail:
1. Log error cụ thể
2. Re-prompt Opus với error context: "Plan invalid vì: {error}. Fix và re-generate."
3. Max 2 retries
4. Nếu vẫn fail → báo anh

---

## Khi nào dùng AoT Planner

**Dùng khi:**
- Task có ≥ 3 steps rõ ràng
- Output của step trước là input của step sau
- Cần spawn nhiều agents
- Cần QA sau khi làm xong
- Task có thể fail → cần biết fail ở atom nào

**Không cần khi:**
- Task 1-2 bước
- Không cần multi-agent
- Simple Q&A

## Category
automation

## Trigger

Use this skill when:
- Task phức tạp cần breakdown thành atoms
- Cần lên plan có dependency graph
- User says: "lên plan phức tạp", "breakdown task", "atom of thought", "AoT plan"
