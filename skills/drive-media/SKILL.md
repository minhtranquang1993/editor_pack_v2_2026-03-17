---
name: drive-media
description: >-
  Lưu media lên Google Drive thay vì workspace local, auto-index bằng SQLite để search/list nhanh.
  Use when user asks upload/search/list media on Drive, "đăng media", "lục ảnh/video/audio", hoặc cần trả link Drive.
---

# Drive Media Skill

## Mục tiêu

- Giảm tải VPS local storage
- Media nằm trên Drive, output trả link Drive
- Search/list nhanh bằng SQLite index local (`memory/media.db`)

## Setup (đã làm)

Root folder:
- `10zSTVA177sS9fgVhJXm8AWX7GrMEyiMr`

Subfolders:
- `image` → `1mirXwo08tkZEtWtGjY002Dccu5AcG46b`
- `video` → `1Sh2pLmP8HQf9C3-h1_w7p6quN0OPYEnU`
- `audio` → `1LHlqnq0wWtmCeQJgMDjdWRL-t_j0lydA`
- `text`  → `1yLykR1F5xd9FM4bCyfzaVeKKxSoqvmon`

Config file:
- `credentials/drive_media_config.json`

Index DB:
- `memory/media.db`

## Commands

### Init (only when root changed)
```bash
python3 tools/drive_media_tools.py init --root-folder-id 10zSTVA177sS9fgVhJXm8AWX7GrMEyiMr
```

### Upload + auto-index
```bash
python3 tools/drive_media_tools.py upload --file "/path/file.jpg" --type image --tags "bé Dung,sinh nhật"
```

### Search
```bash
python3 tools/drive_media_tools.py search --q "bé dung" --type image --limit 10
```

### List recent
```bash
python3 tools/drive_media_tools.py list --type video --limit 20
```

### Reindex from Drive
```bash
python3 tools/drive_media_tools.py reindex
```

## Rule

- Khi user yêu cầu lưu media: luôn upload Drive trước, hạn chế giữ local.
- Khi user hỏi tìm ảnh/video/audio: dùng search/list trên SQLite index.
- Trả kết quả bằng Drive link (`web_view_link`).

## Mesh Connections
- **← yt-content**: Upload video/audio output lên Drive
- **← linkedin**: Upload image cho bài đăng
- **← content-factory**: Lưu article HTML lên Drive
- **← sumvid**: Upload transcript/audio lên Drive

## Output Contract (Tier-3)

**Output bắt buộc:**
- Kết quả upload/search/list rõ ràng
- Link Drive hoặc file id
- Metadata chính (type/tags/thời gian)

**Definition of Done:**
- Anh mở được link và tìm lại được file qua query.

## Category
automation

## Trigger

Use this skill when:
- Cần upload/download file từ Google Drive
- Tìm kiếm ảnh hoặc media trên Drive
- User says: "upload Drive", "lưu ảnh Drive", "tìm ảnh Drive", "download từ Drive"
