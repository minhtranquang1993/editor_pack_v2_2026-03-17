---
name: skill-catalog-audit-lite
description: Audit and classify local skills automatically. Use when reviewing skill coverage, finding overlaps/gaps, or deciding which skills to improve first.
---

# Skill Catalog Audit Lite

Mục tiêu: quét toàn bộ skill local để biết mạnh/yếu ở đâu.

## Use script
- `python3 tools/scan_skills_local.py`
- Output: `memory/skill-catalog-report.md`

## What it checks
- Danh sách skill hiện có
- Có/không có YAML frontmatter
- Có/không có scripts/references
- Nhóm category theo tên
- Gợi ý overlap/gap cơ bản

## Use cases
- Trước khi tạo skill mới
- Review định kỳ mỗi tuần
- Chuẩn bị tối ưu token/context cho skill set

## Category
quality-ops

## Trigger

Use this skill when:
- Cần audit danh sách skills hiện có
- Tìm skills trùng lặp hoặc không dùng
- User says: "audit skills", "review skill list", "tìm skill trùng", "skill catalog"