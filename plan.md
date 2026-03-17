# Editor Pack v2 2026-03-17 — Implementation Plan

Based on [EDITOR_README.md](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/EDITOR_README.md).

## Current State

The repo `editor_pack_v2_2026-03-17` contains only:
- `EDITOR_README.md` — spec for 3 tasks (P1/P2/P3)
- `ref_*.py` — reference implementations for tools & scripts
- `p1_skills_missing_scripts_ref.txt`, `p2_hardcoded_paths.txt`, `p3_new_skills_list.txt` — input lists

The actual codebase (`skills/`, `tools/`, `memory/`) must be assembled from:
- `editor_pack_v2_2026-03-16/files/skills/` — 62 skill directories
- `ref_*.py` files — tool & script implementations
- `ref_skill_routing_map_current.md` — current routing map

---

## Phase 0: Build Repo Structure

### Skills
```bash
cp -r editor_pack_v2_2026-03-16/files/skills/ editor_pack_v2_2026-03-17/skills/
cp editor_pack_v2_2026-03-16/files/skill_manifest.json editor_pack_v2_2026-03-17/
```

### Scripts for P1 Skills (create dirs + copy ref scripts)
| Skill | Script Source | Target |
|-------|-------------|--------|
| `ads-insight-auto` | `ref_ads_insight_auto_script.py` | `skills/ads-insight-auto/scripts/ads_insight.py` |
| `hands-framework` | `ref_hands_framework_script.py` | `skills/hands-framework/scripts/hands_core.py` |
| `persistent-memory` | `ref_persistent_memory_script.py` | `skills/persistent-memory/scripts/mem_manager.py` |
| `rag-kit` | `ref_rag_kit_script.py` | `skills/rag-kit/scripts/kb_manager.py` |
| `weekly-review-auto` | `ref_weekly_review_auto_script.py` | `skills/weekly-review-auto/scripts/weekly_review.py` |

### Tools
```bash
mkdir -p editor_pack_v2_2026-03-17/tools/
cp ref_api_key_rotator.py tools/api_key_rotator.py
cp ref_drive_media_tools.py tools/drive_media_tools.py
cp ref_memory_tier.py tools/memory_tier.py
# openclaw_backup.py — check if ref exists, else create placeholder
```

### Memory
```bash
mkdir -p editor_pack_v2_2026-03-17/memory/
cp ref_skill_routing_map_current.md memory/skill-routing-map.md
```

---

## Phase 1: P1 — Add `## Scripts` to 5 SKILL.md files

Per EDITOR_README, only skills with real `.py` scripts get a `## Scripts` section.
Skip skills with only `__init__.py` (`recap`, `brand-analyze`, `debate-review`, `fb-page-comment`, `fb-page-seeding-comment`, `linkedin`).

### 5 SKILL.md files to modify:

#### [MODIFY] [SKILL.md](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/skills/ads-insight-auto/SKILL.md)
Append `## Scripts` section documenting `scripts/ads_insight.py` — Hands-based script, no direct CLI args, runs via `run_hand()`.

#### [MODIFY] [SKILL.md](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/skills/hands-framework/SKILL.md)
Append `## Scripts` section documenting `scripts/hands_core.py` — library, not a CLI tool. Document import pattern: `from hands_core import HandState, HandLogger, send_telegram, run_hand`.

#### [MODIFY] [SKILL.md](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/skills/persistent-memory/SKILL.md)
Append `## Scripts` section documenting `scripts/mem_manager.py` with CLI args:
- `--save --shelf <shelf> --content "..." [--tags "..."] [--force]`
- `--recall "query" [--shelf <shelf>]`
- `--list [--shelf <shelf>]`
- `--stats`
- `--delete <id>`

#### [MODIFY] [SKILL.md](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/skills/rag-kit/SKILL.md)
Append `## Scripts` section documenting `scripts/kb_manager.py` with CLI args:
- `--ingest <url> [--force]`
- `--search "<query>"`
- `--list [--tag <tag>]`
- `--summary`
- `--delete <id>`

#### [MODIFY] [SKILL.md](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/skills/weekly-review-auto/SKILL.md)
Append `## Scripts` section documenting `scripts/weekly_review.py` — Hands-based, key arg `--mode weekly|monthly`.

---

## Phase 2: P2 — Env-aware paths in 4 tools

Replace hardcoded `/root/.openclaw/workspace` with `os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace")`.

#### [MODIFY] [api_key_rotator.py](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/tools/api_key_rotator.py)
```diff
+import os
-STATE_DIR = Path("/root/.openclaw/workspace/memory")
+_WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
+STATE_DIR = _WORKSPACE / "memory"
```

#### [MODIFY] [drive_media_tools.py](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/tools/drive_media_tools.py)
```diff
-WORKSPACE = Path("/root/.openclaw/workspace")
+WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
```
(Note: `os` already imported)

#### [MODIFY] [memory_tier.py](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/tools/memory_tier.py)
```diff
-WORKSPACE = Path("/root/.openclaw/workspace")
+WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/root/.openclaw/workspace"))
```
(Add `import os` at top)

#### [MODIFY] [openclaw_backup.py](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/tools/openclaw_backup.py)
Check for any hardcoded paths and apply same pattern. If no file exists in the v2_2026-03-16 repo, check if `openclaw-backup` skill exists and extract the tool from there.

---

## Phase 3: P3 — Update skill-routing-map.md

#### [MODIFY] [skill-routing-map.md](file:///Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17/memory/skill-routing-map.md)

1. Read all 65 new skills' SKILL.md files for description + trigger
2. Add entries to the routing table categorized by task type
3. Update header: `Last updated: 2026-03-17`
4. Preserve all existing entries

---

## Verification Plan

### P1 Verification
```bash
cd /Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17

# Check 5 skills have ## Scripts
for skill in ads-insight-auto hands-framework persistent-memory rag-kit weekly-review-auto; do
  echo "=== $skill ==="
  grep -c "## Scripts" skills/$skill/SKILL.md
done
# Expected: each = 1

# Check __init__-only skills unchanged
for skill in recap brand-analyze debate-review fb-page-comment fb-page-seeding-comment linkedin; do
  echo "=== $skill ==="
  grep -c "## Scripts" skills/$skill/SKILL.md 2>/dev/null || echo "not found (expected)"
done
# Expected: each = 0 or "not found"
```

### P2 Verification
```bash
cd /Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17

# Syntax check
python3 -m py_compile tools/api_key_rotator.py
python3 -m py_compile tools/memory_tier.py

# Env pattern check
grep -c 'os.environ.get("OPENCLAW_WORKSPACE"' tools/api_key_rotator.py tools/drive_media_tools.py tools/memory_tier.py
# Expected: each = 1

# No remaining hardcoded paths (except in fallback string)
grep -c '= Path("/root/.openclaw/workspace")' tools/api_key_rotator.py tools/drive_media_tools.py tools/memory_tier.py
# Expected: each = 0

# Functional test (memory_tier.py --help should work)
OPENCLAW_WORKSPACE=/tmp/test python3 tools/memory_tier.py --help
```

### P3 Verification
```bash
cd /Users/minhtqm1993/.gemini/antigravity/scratch/editor_pack_v2_2026-03-17

# Header date
grep "Last updated: 2026-03-17" memory/skill-routing-map.md

# Count skills in routing map (should be >= 66)
grep -c '`' memory/skill-routing-map.md
```

---

## Commit & Push
- Commit message: `fix: editor_pack_v2_2026-03-17 — scripts refs + env paths + routing map`
- Push to `https://github.com/minhtranquang1993/editor_pack_v2_2026-03-17`
