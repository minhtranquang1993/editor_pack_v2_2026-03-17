# Editor Pack v2 — 2026-03-17

> Separate from editor_pack_2026-03-17 (P1/P2/P3).
> 3 new tasks found from deep scan this session.

## Summary

| # | Priority | Task | Scope |
|---|----------|------|-------|
| P1 | 🟡 Medium | SKILL.md scripts cross-reference | 11 skills |
| P2 | 🟡 Medium | Hardcoded workspace paths → env-aware | 4 files |
| P3 | 🟢 Low | skill-routing-map.md update | 1 file |

---

## P1 🟡 — Add scripts cross-reference in 11 SKILL.md files

**Goal:** Each SKILL.md that has a `scripts/` dir with real `.py` files should document
how to use those scripts. Currently 11 SKILL.md files have scripts but don't mention them.

**Input:** `p1_skills_missing_scripts_ref.txt` — list of 11 skills

**Affected skills + their scripts:**
- `ads-insight-auto` → `scripts/ads_insight.py`
- `hands-framework` → `scripts/hands_core.py`
- `persistent-memory` → `scripts/mem_manager.py`
- `rag-kit` → `scripts/kb_manager.py`
- `recap` → `scripts/__init__.py` (skip if empty)
- `weekly-review-auto` → `scripts/weekly_review.py`
- `brand-analyze` → `scripts/__init__.py` (skip if empty)
- `debate-review` → `scripts/__init__.py` (skip if empty)
- `fb-page-comment` → `scripts/__init__.py` (skip if empty)
- `fb-page-seeding-comment` → `scripts/__init__.py` (skip if empty)
- `linkedin` → `scripts/__init__.py` (skip if empty)

**How:**
1. For each skill with a real (non-empty, non-`__init__.py`) scripts/*.py:
   - Read the script to understand its CLI args / main function
   - Add a `## Scripts` section near the bottom of SKILL.md
   - Format: simple usage line, example command, key args
2. For skills with only `__init__.py` (empty placeholder) — skip, no action needed.

**Format:**
```markdown
## Scripts

Run via CLI:
```
python3 skills/{skill-name}/scripts/{script}.py [args]
```
Key args:
- `--arg1`: description
- `--arg2`: description
```

**Acceptance:**
- [ ] `ads-insight-auto`, `hands-framework`, `persistent-memory`, `rag-kit`, `weekly-review-auto` have `## Scripts` section
- [ ] Section is accurate (args match the actual script)
- [ ] Skills with only `__init__.py` are unchanged

---

## P2 🟡 — Make 4 tools use OPENCLAW_WORKSPACE env (not hardcoded paths)

**Goal:** Tools should work on any machine/path, using `OPENCLAW_WORKSPACE` env var
with `/root/.openclaw/workspace` as fallback. 4 files currently hardcode the path directly.

**Files to fix:**
1. `tools/api_key_rotator.py` — line 16: `STATE_DIR = Path("/root/.openclaw/workspace/memory")`
2. `tools/drive_media_tools.py` — line 26: `WORKSPACE = Path("/root/.openclaw/workspace")`
3. `tools/memory_tier.py` — line 17: `WORKSPACE = Path("/root/.openclaw/workspace")`
4. `tools/openclaw_backup.py` — check and fix any hardcoded workspace paths

**How:** For each file, replace hardcoded path with env-aware version:

```python
# Before:
WORKSPACE = Path("/root/.openclaw/workspace")

# After:
import os
WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
```

For `api_key_rotator.py` specifically:
```python
# Before:
STATE_DIR = Path("/root/.openclaw/workspace/memory")

# After:
import os
_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
STATE_DIR = _WORKSPACE / "memory"
```

**Note:**
- Some tools already do this correctly (e.g. `fb_page_comment.py` uses `os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")`) — use those as model.
- Do NOT change logic, only the path resolution.
- Check `openclaw_backup.py` manually — it may have multiple hardcoded paths.

**Acceptance:**
- [ ] All 4 files use `os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")` pattern
- [ ] `OPENCLAW_WORKSPACE=/tmp/test python3 tools/memory_tier.py --help` runs without error
- [ ] No functional change to any tool
- [ ] `python3 tools/regression_suite.py` → all PASS

---

## P3 🟢 — Update skill-routing-map.md (66 skills, last updated 2026-03-10)

**Goal:** `memory/skill-routing-map.md` maps task keywords → recommended skills.
It's been 7 days out of date — 66 skills added since 2026-03-10 are NOT in the map.

**Input:** `p3_new_skills_list.txt` — 65 skills newer than 2026-03-10

**How:**
1. Read current `memory/skill-routing-map.md` to understand format/categories
2. For each of the 65 new skills, read its `SKILL.md` description + trigger section
3. Map it to an appropriate routing category (marketing / seo / automation / ops / memory / etc.)
4. Add entries under correct category
5. Update header: `Last updated: 2026-03-17`

**Note:**
- Keep existing entries (don't remove)
- Match category style of current file
- Each entry format should match what's already in the file (observe before writing)
- Focus on skills with clear `## Trigger` sections first

**Acceptance:**
- [ ] `memory/skill-routing-map.md` — `Last updated: 2026-03-17`
- [ ] All 66 skills appear in at least one routing category
- [ ] Existing entries preserved

---

## General Rules
- Do NOT modify any file outside scope of these 3 tasks
- Keep existing code style/formatting
- Commit message: `fix: editor_pack_v2_2026-03-17 — scripts refs + env paths + routing map`
- Test after P1: check grep in affected SKILL.md
- Test after P2: `python3 tools/regression_suite.py` → all PASS
- P3 can be done last (no test needed beyond manual check)
