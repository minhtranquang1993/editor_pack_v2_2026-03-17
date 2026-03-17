---
name: fb-page-comment
description: Comment bài FB Page DND Sài Gòn theo template có sẵn (text + ảnh từ Google Drive). Use when user sends a FB post URL and asks to comment on it.
---

# FB Page Auto Comment

Comment bài FB Page **Bệnh Viện Mắt Quốc Tế DND Sài Gòn** bằng các template đã cài sẵn trên Google Drive (text + ảnh).

## Trigger Keywords
- "comment bài này [link]"
- "comment bài fb"
- "fb comment"
- "/fb-comment"
- "ní comment bài"
- "comment giúp anh"

## How to Use

### Step 1: Extract Post URL
Extract the Facebook post URL from the user's message. The URL may be in various formats:
- `https://www.facebook.com/PageName/posts/123456`
- `https://www.facebook.com/permalink.php?story_fbid=123&id=456`
- `https://www.facebook.com/photo?fbid=123`
- `https://www.facebook.com/share/p/AbcXyz`

### Step 2: Run the Comment Script

**Full comment (all templates):**
```bash
python3 tools/fb_page_comment.py --post-url "<URL>"
```

**Specific templates only:**
```bash
python3 tools/fb_page_comment.py --post-url "<URL>" --templates 1,2
```

**Dry run (preview without posting):**
```bash
python3 tools/fb_page_comment.py --post-url "<URL>" --dry-run
```

**Force sync templates before commenting:**
```bash
python3 tools/fb_page_comment.py --post-url "<URL>" --force-sync
```

**Sync templates only (no comment):**
```bash
python3 tools/fb_page_comment.py --sync-templates
```

### Step 3: Report Results

After the script completes, report to the user:
- How many comments were posted successfully
- Any errors encountered
- If the post was already commented (idempotent check)

## Output Format

Example success output:
```
✅ Done: 3 comment(s) posted successfully!
```

Example already-commented:
```
⚠️ Đã comment bài này rồi (post_id: xxx)
```

## Error Handling

| Error | Action |
|-------|--------|
| Token expired | Tell user: "FB token hết hạn, cần refresh file `credentials/fb_page_token.txt`" |
| URL not parseable | Ask user to provide a valid FB post URL |
| Rate limited | Script auto-retries 3 times. If still fails, tell user to wait and try again |
| No templates | Run `--sync-templates` first to sync from Google Drive |

## Notes
- Templates (text + images) are managed on Google Drive folder. User edits `comments.json` and uploads images there.
- Script auto-syncs from Drive when cache is >24h old.
- Each post is only commented once (idempotent). To re-comment, remove the entry from `memory/fb_comment_log.json`.

## Category
marketing-ads
