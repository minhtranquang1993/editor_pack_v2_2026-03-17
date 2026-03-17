---
name: antrua
description: >-
  Tra cứu suất ăn trưa của anh Minh tại DND từ email Google Forms. Mỗi tuần có 2 email
  "DND - ĐĂNG KÝ SUẤT ĂN TRƯA" gửi tới minhtqm1993@gmail.com — skill này tìm đúng 2 email
  tuần hiện tại, parse menu, trả lời ngay.
  Trigger: "trưa nay ăn gì", "hôm nay ăn gì", "trưa nay ăn món gì", "menu hôm nay",
  "thứ 5 ăn gì", "cuối tuần ăn gì", "/antrua", hoặc bất kỳ câu hỏi nào về suất ăn trưa DND.
---

# antrua Skill

## Workflow

```
Anh gọi /antrua (quick command)
  │
  ├─ Nếu là THỨ 2 + lần bấm đầu tuần:
  │    → scripts/antrua.py tự thu thập menu tuần từ email
  │    → lưu cache tuần vào memory/antrua_cache.json
  │
  ├─ Các lần bấm sau trong tuần (hoặc ngày khác):
  │    → chỉ đọc cache và báo món hôm nay
  │
  └─ Trả kết quả cho anh
```

## Cách chạy

```bash
# Quick command mặc định (/antrua)
python3 skills/antrua/scripts/antrua.py

# Ép cập nhật lại menu tuần hiện tại
python3 skills/antrua/scripts/antrua.py --refresh

# Ngày cụ thể
python3 skills/antrua/scripts/antrua.py --date T5
python3 skills/antrua/scripts/antrua.py --date 27/02

# Cả tuần
python3 skills/antrua/scripts/antrua.py --all
```

## Parse intent từ câu anh nói

| Anh nói | Dùng flag |
|---|---|
| "trưa nay", "hôm nay ăn gì", "menu hôm nay" | (không flag) |
| "thứ 5 ăn gì", "T5 ăn gì" | `--date T5` |
| "ngày 27 ăn gì", "27/02 ăn gì" | `--date 27/02` |
| "cả tuần ăn gì", "menu tuần này", "/antrua" | `--all` |

## Notes
- Gmail credential: `credentials/google_workspace_token.json` + `credentials/google_workspace_credentials.json`
- Cache tuần lưu tại: `memory/antrua_cache.json`
- Quick mode mặc định: chỉ thứ 2 và lần đầu tuần mới tự fetch email; còn lại đọc cache để báo món hôm nay
- Script tự tìm email tuần hiện tại, không cần chỉ định subject
- Nếu không tìm thấy email → nhắc anh kiểm tra email đăng ký tuần này chưa gửi

## Output Contract (Tier-3)

**Output bắt buộc:**
- Món hôm nay (hoặc theo ngày anh hỏi)
- Nếu anh hỏi cả tuần: danh sách T2-T7
- Nguồn: email/form tuần hiện tại

**Definition of Done:**
- Trả đúng món theo ngày, không nhầm tuần.

## Category
automation
