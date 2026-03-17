---
name: thumb-prj-thanhhung
description: >-
  Tạo/sửa thumbnail cho dự án Thành Hưng (chuyển nhà/văn phòng). Thay text trên
  template Canva gốc bằng Pillow. Trigger: "sửa ảnh thumbnail Thành Hưng",
  "tạo thumbnail Thành Hưng", "đổi text thumbnail", "/thumb-prj-thanhhung".
---

# Thumbnail Thành Hưng

Tạo thumbnail từ template Canva `DAFx3o-osx8` bằng cách thay text overlay.

## Params

- `line1` — Dòng trên cùng (mặc định: "CHUYỂN VĂN PHÒNG TRỌN GÓI")
- `line2` — Địa điểm / text đỏ lớn (**bắt buộc**)
- `hotline` — Số hotline (mặc định: "1800.9097")

## Usage

```bash
# Chỉ đổi địa điểm
python3 scripts/gen_thumbnail.py --line2 "QUẬN 7" --output /path/to/output.png

# Đổi cả title + địa điểm
python3 scripts/gen_thumbnail.py --line1 "CHUYỂN NHÀ TRỌN GÓI" --line2 "BÌNH THẠNH" --output /path/to/output.png

# Dùng cached template (không gọi Canva API)
python3 scripts/gen_thumbnail.py --line2 "THỦ ĐỨC" --output /path/to/output.png --no-canva
```

## Workflow

1. Export ảnh gốc từ Canva API (hoặc dùng cache `assets/template-cache.png`)
2. Phủ trắng vùng text cũ (line1 + line2 + hotline)
3. Vẽ text mới bằng font NotoSans Bold, căn giữa
4. Lưu ảnh PNG chất lượng cao

## Notes

- Template Canva design ID: `DAFx3o-osx8`
- Font: `assets/NotoSans-Variable.ttf`
- Ảnh output: 1366x768 px
- Ưu tiên `--no-canva` để tiết kiệm API call (dùng cache)
- Chỉ gọi Canva API khi template gốc thay đổi

## Output Contract (Tier-3)

**Output bắt buộc:**
- Ảnh thumbnail mới (đúng text yêu cầu)
- Path output
- Xác nhận hotline/địa điểm đã cập nhật đúng

**Definition of Done:**
- Thumbnail dùng được ngay cho đăng bài/campaign.

## Category
automation
