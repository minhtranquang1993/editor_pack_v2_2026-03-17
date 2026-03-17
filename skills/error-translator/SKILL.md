---
name: error-translator
description: Translate technical errors into plain Vietnamese with direct fixes and alternatives. Use when logs/commands fail and the user needs quick, non-jargon troubleshooting guidance.
---

# 📋 SKILL: Error Translator
# Location: /root/.openclaw/workspace/skills/error-translator/

## Mô tả
Dịch lỗi kỹ thuật sang ngôn ngữ đời thường + gợi ý fix ngay.
Tự động kích hoạt khi có error message xuất hiện trong conversation.

---

## Trigger
- Anh paste error message
- Output tool/exec trả về lỗi
- Anh nói "bị lỗi", "lỗi gì", "sao không chạy được"

---

## Output Format

```
❌ Lỗi: [mô tả người thường hiểu được]
   └─ Gốc: [snippet lỗi gốc, tối đa 1 dòng]

💡 Fix: [bước fix cụ thể, ngắn gọn]
   └─ Hoặc: [cách fix thay thế nếu có]
```

---

## Error Database

### Shell / System
| Pattern | Mô tả | Fix |
|---------|-------|-----|
| `command not found` | Chưa cài chương trình này | `apt install [tên]` hoặc check PATH |
| `Permission denied` | Không có quyền truy cập | Thêm `sudo` hoặc `chmod` |
| `No such file or directory` | File/folder không tồn tại | Kiểm tra đường dẫn, tạo folder nếu thiếu |
| `Connection refused` | Service chưa chạy | Start service: `systemctl start [tên]` |
| `Address already in use` | Port đang bị chiếm | Kill process cũ: `lsof -i :[port]` |
| `Disk quota exceeded` / `No space left` | Hết dung lượng ổ đĩa | Dọn dẹp file cũ, xóa logs |
| `SIGKILL` / `OOM` | Hết RAM | Tăng swap hoặc giảm load |

### Python / pip
| Pattern | Mô tả | Fix |
|---------|-------|-----|
| `ModuleNotFoundError` | Thiếu thư viện | `pip install [tên]` |
| `IndentationError` | Sai khoảng trắng trong code | Kiểm tra tab vs space |
| `SyntaxError` | Code viết sai cú pháp | Kiểm tra dấu ngoặc, dấu hai chấm |
| `TypeError` | Dùng sai kiểu dữ liệu | Kiểm tra biến truyền vào |
| `KeyError` | Key không tồn tại trong dict | Dùng `.get()` thay vì `[]` |
| `FileNotFoundError` | File không tồn tại | Kiểm tra đường dẫn |
| `RecursionError` | Vòng lặp vô hạn | Kiểm tra điều kiện dừng |

### Node.js / npm
| Pattern | Mô tả | Fix |
|---------|-------|-----|
| `Cannot find module` | Thiếu package | `npm install` |
| `EACCES` | Không có quyền | Sửa permissions hoặc dùng nvm |
| `ENOSPC` | Hết disk | Dọn node_modules |
| `npm ERR! peer dep` | Phiên bản không tương thích | Update package.json |
| `Maximum call stack` | Vòng lặp vô hạn | Kiểm tra điều kiện dừng |

### Git
| Pattern | Mô tả | Fix |
|---------|-------|-----|
| `conflict` | Code bị xung đột với nhánh khác | Merge conflict thủ công |
| `rejected` | Push bị từ chối | `git pull` trước rồi push lại |
| `not a git repository` | Chưa init git | `git init` |
| `detached HEAD` | Không ở branch nào | `git checkout main` |
| `Authentication failed` | Sai credentials | Kiểm tra token/password |

### API / Network
| Pattern | Mô tả | Fix |
|---------|-------|-----|
| `401 Unauthorized` | Sai API key hoặc hết hạn | Kiểm tra lại API key |
| `403 Forbidden` | Không có quyền truy cập endpoint này | Kiểm tra permissions |
| `404 Not Found` | URL không tồn tại | Kiểm tra lại URL/endpoint |
| `429 Too Many Requests` | Gọi API quá nhiều | Chờ hoặc giảm frequency |
| `500 Internal Server Error` | Lỗi phía server | Thử lại, hoặc báo provider |
| `CORS` | Website chặn request từ domain khác | Cấu hình CORS headers |
| `ECONNREFUSED` | Không kết nối được server | Kiểm tra server có đang chạy không |
| `ETIMEDOUT` | Kết nối quá chậm | Kiểm tra mạng, tăng timeout |
| `SSL/TLS` | Chứng chỉ HTTPS lỗi | Check cert hoặc dùng HTTP (dev) |

### OpenClaw / AI specific
| Pattern | Mô tả | Fix |
|---------|-------|-----|
| `model not found` | Model ID sai | Kiểm tra case-sensitive (lowercase) |
| `context_length_exceeded` | Tin nhắn quá dài | Tóm tắt lại hoặc /new session |
| `rate_limit_exceeded` | Gọi API quá nhiều | Chờ vài giây rồi thử lại |
| `invalid api key` | API key sai | Kiểm tra lại key trong config |
| `tool call failed` | Tool bị lỗi | Xem log chi tiết, thử lại |

---

## Fallback
Nếu không match pattern nào:
```
❌ Lỗi: Có vấn đề xảy ra — em chưa nhận ra lỗi này.
💡 Fix: Anh paste full error message cho em xem nhé, em sẽ debug!
```

---

## Security
- Sanitize error messages — không expose passwords, tokens trong output
- Nếu lỗi chứa credentials → hiển thị "[REDACTED]"

## Response Template Pack (Tier-3)

### Lỗi chuẩn
```text
❌ Lỗi: ...
💡 Vì sao: ...
🛠 Cách xử lý nhanh: ...
🔁 Nếu vẫn lỗi: ...
```

## Definition of Done (Tier-3)
- Có nguyên nhân dễ hiểu + hướng xử lý cụ thể.
- Không chỉ dán log, phải có hành động tiếp theo.

## Category
quality-ops
