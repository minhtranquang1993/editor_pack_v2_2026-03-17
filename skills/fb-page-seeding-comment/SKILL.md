---
name: fb-page-seeding-comment
description: Seeding comment Facebook bằng nhiều Page phụ theo vòng xoay nội dung (mỗi page chỉ comment 1 lần cho mỗi bài). Dùng khi anh nói "seeding bài link", "seeding post", hoặc cần comment đa page vào 1 link bài viết Facebook. Khác flow cũ `fb-page-comment` (trigger: "comment ads link").
---

# FB Page Seeding Comment (Multi-Page)

## Mục tiêu
Seeding 1 bài Facebook bằng nhiều Page phụ của anh:
- Mỗi page comment **1 lần/bài**
- Nội dung comment **khác nhau** giữa các page trong cùng bài
- Nội dung xoay vòng theo pool template

## Trigger mapping
- Trigger skill này: `seeding bài link`, `seeding post`, `seeding bài`
- Trigger skill cũ (`fb-page-comment`): `comment ads link`

## Cách chạy (khi editor code xong)
```bash
python3 tools/fb_page_seeding_comment.py --post-url "<FB_POST_URL>"
```

Tuỳ chọn:
```bash
python3 tools/fb_page_seeding_comment.py --post-url "<FB_POST_URL>" --dry-run
python3 tools/fb_page_seeding_comment.py --post-url "<FB_POST_URL>" --max-pages 4
python3 tools/fb_page_seeding_comment.py --post-url "<FB_POST_URL>" --force-content-reset
```

## File contract bắt buộc
- `credentials/fb_seeding_pages.json` — danh sách page + token (nhiều page)
- `memory/fb_seeding_templates.json` — pool nội dung comment (editor bổ sung sau)
- `memory/fb_seeding_state.json` — state xoay vòng nội dung
- `memory/fb_seeding_log.json` — log kết quả/idempotency
- `docs/specs/fb-page-seeding-comment-spec.md` — đặc tả kỹ thuật đầy đủ

## Ghi chú
- Tuyệt đối không hardcode token vào script.
- Nếu thiếu token/page nào thì skip page đó, vẫn chạy các page còn lại.
- Nếu bài đã seeding đủ page theo log thì không comment lại trùng.

## Category
marketing-ads
