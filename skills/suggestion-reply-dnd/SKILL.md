---
name: suggestion-reply-dnd
description: Gợi ý cách trả lời tin nhắn inbox Messenger Page DND dựa trên lịch sử hội thoại thực tế. Anh Minh hỏi "khách hỏi X thì trả lời sao?" → em tìm trong inbox những cuộc hội thoại tương tự, tổng hợp cách admin đã từng trả lời, đề xuất câu trả lời phù hợp. Lâu lâu anh cần cào thêm inbox mới → dùng lệnh update. Trigger: "trả lời sao nếu...", "khách hỏi...", "/suggestion-reply", "update inbox".
---

# Skill: suggestion-reply-dnd

## Mô tả
Skill này giúp anh Minh nhanh chóng có câu trả lời chuẩn khi khách hàng hỏi các vấn đề trong Messenger inbox DND. Dữ liệu được học từ lịch sử inbox thực tế.

## Trigger
- "trả lời sao nếu khách hỏi [X]"
- "khách hỏi [X] thì nói gì"
- "reply kiểu gì khi [X]"
- "/suggestion-reply [câu hỏi]"
- "update inbox" / "cào inbox mới"

## Workflow

### Mode 1: Gợi ý câu trả lời (Query)

1. Nhận câu hỏi từ anh (mô tả tình huống hoặc nội dung khách nhắn)
2. Chạy script tìm kiếm trong SQLite:
```bash
python3 tools/suggestion_reply_dnd.py --query "<câu hỏi của anh>"
```
3. Script trả về top 3-5 cuộc hội thoại tương tự + cách admin đã trả lời
4. Em tổng hợp → đề xuất 2-3 phương án trả lời theo tone DND

### Mode 2: Update inbox (Crawl)

Khi anh nói "update inbox" hoặc "cào inbox mới":
```bash
python3 tools/suggestion_reply_dnd.py --update [--limit 100]
```
- Mặc định cào 200 cuộc hội thoại gần nhất
- Chỉ insert tin nhắn mới (không duplicate)
- Báo anh số tin nhắn đã thêm

### Mode 3: Xem thống kê

```bash
python3 tools/suggestion_reply_dnd.py --stats
```
Hiển thị: tổng conversations, tổng messages, ngày cập nhật lần cuối

## Output Contract

**Khi gợi ý reply:**
```
🔍 Tìm thấy X cuộc hội thoại liên quan

📌 Tình huống tương tự:
- [Khách hỏi]: "..."
- [Admin đã trả lời]: "..."

✍️ Gợi ý trả lời:
1. [Phương án 1 — ngắn gọn]
2. [Phương án 2 — chi tiết hơn]
3. [Phương án 3 — nếu cần hẹn gặp/gọi điện]
```

**Khi update:**
```
✅ Đã thêm X cuộc hội thoại mới (Y tin nhắn)
📊 Tổng DB: Z conversations | W messages
📅 Cập nhật lần cuối: YYYY-MM-DD HH:MM
```

## Notes
- DB lưu tại: `memory/suggestion_reply_dnd.db` (SQLite)
- Token dùng: `credentials/fb_page_token.txt` (Page Access Token)
- Page ID: `104552934399242`
- Không lưu tên/ID khách hàng ra ngoài DB (privacy)
- Nếu DB chưa tồn tại → chạy `--init` trước

## Category
marketing-ads
