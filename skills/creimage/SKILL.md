---
name: creimage
description: Tạo ảnh bằng model gemini-3-pro-image qua API minai93 (chat/completions hoặc responses), lưu file PNG/JPG vào workspace và trả đường dẫn ảnh. Use when user asks tạo ảnh từ prompt, test model gemini image, hoặc cần sinh nhiều biến thể ảnh từ mô tả tiếng Việt/Anh.
---

# CreImage (Gemini 3 Pro Image)

Tạo ảnh trực tiếp từ prompt bằng model `gemini-3-pro-image` và lưu vào `outputs/creimage/`.

## 1) Quick command

```bash
python3 skills/creimage/scripts/generate_image.py \
  --prompt "một chú mèo cam dễ thương đang ngồi bàn làm việc, flat illustration" \
  --output outputs/creimage/cat-flat.jpg
```

## 2) Dùng prompt nâng chất lượng

- Mô tả rõ: subject + style + lighting + background
- Nếu cần text trên ảnh: ghi rõ chính tả + vị trí
- Nên thêm ràng buộc: `no watermark`, `clean composition`, `high detail`

Ví dụ:

```bash
python3 skills/creimage/scripts/generate_image.py \
  --prompt "Poster tối giản về vận chuyển văn phòng, tone xanh dương, icon thùng carton, chữ: 'Chuyển văn phòng nhanh gọn', no watermark" \
  --output outputs/creimage/poster-office.jpg
```

## 3) Tham số

- `--prompt` (bắt buộc): mô tả ảnh
- `--output` (optional): đường dẫn file đầu ra (`.jpg`/`.jpeg`/`.png`)
- `--model` (optional): mặc định `gemini-3-pro-image`
- `--base-url` (optional): mặc định `https://minai93.duckdns.org/v1`
- `--api-key` (optional): ưu tiên env `MINAI93_API_KEY`, fallback `minai93-key-1`
- `--endpoint` (optional): `chat` (mặc định) hoặc `responses`

## 4) Lỗi thường gặp

- `unknown provider for model minai93/gemini-3-pro-image`:
  - Không dùng prefix `minai93/` trong payload model.
  - Dùng đúng: `gemini-3-pro-image`.
- Không có `images` trong response:
  - Prompt bị chặn safety hoặc provider fail tạm thời → đổi prompt và thử lại.
- Data URL decode fail:
  - Provider trả format lạ → thử endpoint `--endpoint responses`.

## 5) Output

Script in ra JSON:

```json
{
  "ok": true,
  "model": "gemini-3-pro-image",
  "endpoint": "chat",
  "output": "outputs/creimage/cat-flat.jpg",
  "bytes": 123456
}
```

Nếu lỗi, script trả exit code != 0 và in JSON có `error` để debug nhanh.

## Output Contract (Tier-3)

**Output bắt buộc:**
- Ảnh tạo thành công + đường dẫn file
- Prompt đã dùng (rút gọn)
- Trạng thái model/endpoint (chat|responses)

**Definition of Done:**
- Có file ảnh hợp lệ và gửi được cho anh.

## Category
automation

## Trigger

Use this skill when:
- Cần tạo/sinh ảnh từ prompt
- User yêu cầu generate hình ảnh
- User says: "tạo ảnh", "sinh ảnh", "generate image", "vẽ ảnh"
