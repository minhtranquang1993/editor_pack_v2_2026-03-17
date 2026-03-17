---
name: market-data
description: Validate market data responses (giá vàng, chứng khoán, tỷ giá, bitcoin...) với timestamp + source enforcement. Trigger khi anh hỏi về giá cả thị trường.
---

# Market Data Skill

## Trigger Keywords
- "giá vàng"
- "giá USD"
- "chứng khoán"
- "VN-Index"
- "giá bitcoin"
- "tỷ giá"
- "giá bạc"
- "giá dầu"
- "crypto"

## Behavior

Khi user hỏi về giá thị trường (vàng, ngoại tệ, chứng khoán, crypto), skill này:

1. Thu thập dữ liệu từ nguồn (search, API, hoặc cache)
2. Gọi `scripts/market_lookup.py` để validate và format response
3. Đảm bảo mọi response đều có:
   - **Nguồn** (source): tên tổ chức/website cung cấp dữ liệu
   - **Thời gian cập nhật** (timestamp): thời điểm dữ liệu được lấy
   - **Độ tin cậy** (confidence): dựa trên độ tươi của dữ liệu
4. Nếu thiếu nguồn hoặc thời gian → tự động gắn nhãn cảnh báo

## Usage

```bash
python3 scripts/market_lookup.py \
    --asset-name "Giá vàng SJC" \
    --value "89,200,000 VND/lượng" \
    --source "SJC" \
    --timestamp "2026-03-06 10:00"
```

## Output Format

```
💰 Giá vàng SJC: 89,200,000 VND/lượng
🕐 Cập nhật: 2026-03-06 10:00
📡 Nguồn: SJC
🎯 Độ tin cậy: CAO ✅
```

## Guardrail Rules

- Không trả số "ảo" không có timestamp/source
- Dữ liệu > 15 phút: cảnh báo mức tin cậy trung bình
- Dữ liệu > 30 phút: cảnh báo mức tin cậy thấp
- Nhiều nguồn mâu thuẫn > 2%: cảnh báo chênh lệch

## Category
automation
