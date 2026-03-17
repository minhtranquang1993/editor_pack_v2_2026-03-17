---
name: openclaw-backup
description: Backup toàn bộ workspace + config OpenClaw (encrypted AES-256) lên Google Drive. Use when: cần backup thủ công, hoặc cron tự động chạy hàng tuần.
---

# OpenClaw Backup

Tạo encrypted backup (AES-256-CBC, PBKDF2) toàn bộ workspace và upload lên Google Drive.

## Usage

### Manual backup
```bash
python3 tools/openclaw_backup.py --drive-folder-id <FOLDER_ID>
```

### With config (no args needed)
```bash
python3 tools/openclaw_backup.py
```
Reads `drive_folder_id` from `credentials/backup_config.json`.

### Force backup (skip min-days check)
```bash
python3 tools/openclaw_backup.py --min-days 0
```

## Configuration

### Passphrase
- Path: `credentials/openclaw_backup_passphrase.txt`
- Auto-generated on first run if missing
- Permissions: `0600`

### Drive folder
- Config file: `credentials/backup_config.json`
- Format:
```json
{
  "drive_folder_id": "<YOUR_FOLDER_ID>"
}
```

### Default behavior
- `--min-days 6`: skip backup if last backup < 6 days ago
- Override with `--min-days 0` to force

## Cron Schedule (gợi ý)
```
0 20 * * 0
```
→ 20:00 UTC Chủ nhật = 3h sáng ICT thứ 2

## Trigger Keywords
- "backup workspace"
- "backup openclaw"
- "/backup"

## Category
automation

## Risk
low
