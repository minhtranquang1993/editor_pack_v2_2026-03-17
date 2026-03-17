---
name: linkedin
description: Tạo content LinkedIn cho Minh đại ca (ghost writer) + đăng bài ngay hoặc schedule. Trigger khi anh nói "viết bài LinkedIn", "đăng LinkedIn", "lên content LinkedIn", "/linkedin". Persona: Senior Digital Marketing Trần Quang Minh, 8+ năm kinh nghiệp, chuyên performance ads. Xem references/persona.md để biết đầy đủ tone/hashtag/format.
---

# LinkedIn Skill

## Workflow

### 1. Tạo content (Create)
Khi anh gửi ý tưởng / chủ đề:
1. **Review** nội dung — xem references/persona.md để check tone + checklist
   - Xem `references/style-dimensions-power-words.md` cho Style Dimensions (LinkedIn profile) + Power Words
2. **Nếu chưa đủ "thịt"** → báo anh cần bổ sung gì cụ thể
3. **Nếu OK** → viết theo giọng Minh Trần, thêm hashtag đúng format
4. **Preview** cho anh xem trước khi hỏi muốn đăng ngay hay schedule

### 2. Đăng bài (Post)
Sau khi anh approve nội dung, hỏi:
- **Đăng ngay** → chạy lệnh post bên dưới
- **Schedule** → hỏi giờ muốn đăng (theo khung giờ vàng: 7-9h / 12-13h / 19-21h ICT)

```bash
# Đăng ngay
python3 tools/linkedin_tools.py --post "<nội dung bài viết>"

# Verify kết nối
python3 tools/linkedin_tools.py --verify
```

### 3. Mở rộng tương lai
Khi anh muốn thêm platform (Threads, Facebook, Blog...):
- Threads: `python3 tools/threads_tools.py --post "<nội dung>"`
- Tạo skill riêng tương tự skill này cho từng platform

## Lưu ý
- Đọc references/persona.md trước khi viết bất kỳ bài nào
- Bài dở → không đăng, báo anh thẳng thắn
- Tối đa 1-2 bài/ngày

## Output Contract (Tier-2)

**Output bắt buộc:**
- Hook mở đầu
- Nội dung chính (có cấu trúc đọc dễ)
- CTA cuối bài
- 3-5 hashtags
- Nếu có lịch đăng: thời gian đề xuất

**Definition of Done:**
- Post đăng được ngay (không cần chỉnh lớn)
- Tone đúng persona Minh, rõ mục tiêu bài viết

## Category
content-seo
