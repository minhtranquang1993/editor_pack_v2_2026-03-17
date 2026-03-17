---
name: content-factory
description: Orchestrated SEO content pipeline with state tracking, artifact validation, and automated review gates.
---

# Content Factory Skill

End-to-end SEO content production pipeline with fail-fast validation, dual review gates, and artifact tracking.

## Pipeline Flow

```
Research → Outline → Gate 1 Review → Write → QA → Gate 2 Review → User Approval → Publish
```

Each stage produces mandatory artifacts stored under `memory/content-pipeline/<keyword-slug>/`.

---

## Execution Helpers

Three Python scripts automate validation and gate decisions:

### 1. Preflight Check

Validates required inputs before starting the pipeline.

```bash
python skills/content-factory/scripts/preflight_check.py \
  --json '{"keyword":"best-seo-tools","search_intent":"informational","country":"VN","language":"vi","brand":"DND"}'
```

### 2. Review Gate Parser

Parses score and verdict from Gate 1 / Gate 2 review reports.

```bash
python skills/content-factory/scripts/review_gate_parser.py \
  --file memory/content-pipeline/<slug>/outline-review-report.md
```

### 3. Pipeline Artifact Validator

Checks all 9 required files + `status.json` schema integrity.

```bash
# Single keyword
python skills/content-factory/scripts/validate_pipeline_artifacts.py \
  --slug <keyword-slug>

# Batch validation
python skills/content-factory/scripts/validate_pipeline_artifacts.py \
  --dir memory/content-pipeline --batch
```

---

## Fail-fast Rules

1. **Preflight failure** → Pipeline does NOT start. Fix inputs and re-trigger.
2. **Gate failure** → Retry up to `max_attempts` (default 2). After exhausting retries, state transitions to `failed`.
3. **Artifact validation failure** → Pipeline is NOT marked as done. Missing files must be generated before proceeding.

---

## Definition of Done

A keyword pipeline is complete when:

1. All 9 required artifacts exist in `memory/content-pipeline/<slug>/`
2. `status.json` has valid schema with state `approved` or `published`
3. `validate_pipeline_artifacts.py --slug <slug>` exits with code 0

```bash
python skills/content-factory/scripts/validate_pipeline_artifacts.py --slug <keyword-slug>
# Expected: exit 0, [<slug>] PASS ✅
```

## Category
content-seo
