---
name: ab-test-tracker
description: "Theo dõi A/B test ads có hệ thống — đăng ký test mới, ghi nhận kết quả hằng ngày, tự động xác định winner khi đủ data, lưu lịch sử để reference sau. Dùng cho Digital Marketing test creative, audience, landing page trên FB/TikTok/Google."
---

# A/B Test Tracker Skill

## Category
marketing-ads


## Tóm tắt
Skill này giúp anh Minh (Senior Digital Marketing tại DND) quản lý A/B test ads một cách có hệ thống:
- Tạo test mới với hypothesis, variant A/B, metric chính
- Cập nhật kết quả hằng ngày (cost, leads, clicks)
- Tự động phát hiện winner khi đủ điều kiện (>15% hiệu suất, min 3 ngày, min 50 leads/variant)
- Gửi alert Telegram khi có winner
- Xem lịch sử test để reference sau

## Storage
- **File:** `~/.openclaw/workspace/ab-tests/tests.json` (main database)
- **Schema:** `references/ab-test-schema.md` (chi tiết cấu trúc)

---

## Workflows

### 1. Tạo Test Mới: `/ab-new`

**Input:**
```
/ab-new
name="Creative Test Week 48"
platform="facebook"
hypothesis="Creative với call-to-action rõ ràng sẽ có CPL thấp hơn"
variant_a="Creative A: Ảnh sản phẩm + CTA 'Đặt lịch tư vấn'"
variant_b="Creative B: Video UGC + CTA 'Xem kết quả'"
primary_metric="cpl"
start_date="2026-03-10"
end_date="2026-03-17"
min_sample=50
```

**Process:**
1. Validate input (tên unique, metric trong [cpl, ctr, cpc, cvr], dates hợp lệ)
2. Tạo test record với status="running"
3. Gán test_id (UUID hoặc auto-increment)
4. Lưu vào `tests.json`
5. Trả lại test_id + confirm message

**Output:**
```json
{
  "status": "created",
  "test_id": "test_001",
  "name": "Creative Test Week 48",
  "start_date": "2026-03-10",
  "end_date": "2026-03-17"
}
```

---

### 2. Update Kết Quả Hằng Ngày: `/ab-update`

**Input:**
```
/ab-update
test_id="test_001"
date="2026-03-10"
variant_a_cost=500000
variant_a_leads=15
variant_a_clicks=120
variant_a_impressions=1200
variant_b_cost=480000
variant_b_leads=18
variant_b_clicks=130
variant_b_impressions=1180
```

**Process:**
1. Validate test_id exists + status="running"
2. Calculate metrics:
   - CPL = cost / leads
   - CPC = cost / clicks
   - CTR = clicks / impressions
3. Tạo daily snapshot record
4. Lưu vào `tests.json` → daily_data array
5. **Auto-check winner:** nếu thỏa điều kiện → trigger winner_detected
6. Trả lại summary

**Output:**
```json
{
  "status": "updated",
  "test_id": "test_001",
  "date": "2026-03-10",
  "variant_a_cpl": 33333.33,
  "variant_b_cpl": 26666.67,
  "variant_b_ahead": "20%"
}
```

---

### 3. Xác Định Winner (Tự động)

**Điều kiện winner** (tất cả phải thỏa):
- Min 3 ngày dữ liệu
- Min 50 leads mỗi variant (tính tổng từ daily data)
- 1 variant vượt trội >15% trên primary_metric
- Hiệu suất ổn định (không dao động liên tục)

**Logic:**
```
Nếu (ngày >= 3) AND (variant_a_leads >= 50 AND variant_b_leads >= 50):
    diff = abs(variant_a_metric - variant_b_metric) / min(variant_a_metric, variant_b_metric) * 100
    if diff > 15%:
        winner = variant_a hoặc variant_b (tùy metric nào tốt hơn)
        confidence = 85% (simple confidence score)
        status = "completed"
        → Gửi Telegram alert + lưu result record
```

**Telegram Alert:**
```
🎯 A/B Test Winner: Creative Test Week 48

📊 Metric: CPL (Cost Per Lead)
🏆 Winner: Creative B
📈 Improvement: +20% (CPL: 26,667 vs 33,333)
⏱️ Duration: 3 ngày
📊 Samples: 50 leads mỗi variant

Recommendation: Scale Creative B, pause Creative A
```

---

### 4. Xem Tests Đang Chạy: `/ab-status`

**Input:**
```
/ab-status
```

**Process:**
1. Đọc từ `tests.json`
2. Filter theo status (mặc định "running", có option "--all" để xem cả completed)
3. Tính tiến độ: (days_run / total_days) %
4. Format thành bảng hoặc list dễ đọc

**Output:**
```
🔄 A/B Tests Đang Chạy (2)

1️⃣ Creative Test Week 48 (test_001)
   Platform: Facebook
   Metric: CPL
   Progress: 3/7 ngày (43%)
   Variant A: 15 leads | CPL: 33,333
   Variant B: 18 leads | CPL: 26,667
   Status: Dữ liệu đủ, Variant B đang dẫn 20%

2️⃣ Audience Test TikTok (test_002)
   Platform: TikTok
   Metric: CTR
   Progress: 1/5 ngày (20%)
   Variant A: 5 leads
   Variant B: 3 leads
   Status: Còn sớm, chưa thể kết luận
```

---

### 5. Xem Lịch Sử Tests: `/ab-history`

**Input:**
```
/ab-history
limit=10
```

**Process:**
1. Đọc từ `tests.json`
2. Filter completed tests
3. Sort by completed_date DESC
4. Limit (mặc định 10)
5. Format + hiển thị kết quả

**Output:**
```
📋 A/B Test History (Hoàn thành)

1. Creative Test Week 47
   Platform: Facebook | Metric: CPL
   Winner: Creative A | Improvement: +18%
   Duration: 7 ngày | Completed: 2026-03-03

2. Landing Page Test
   Platform: Google | Metric: CVR
   Winner: LP B | Improvement: +25%
   Duration: 5 ngày | Completed: 2026-02-28

[Xem tất cả: /ab-history --all]
```

---

## Implementation Details

### Data Storage (tests.json)
```json
{
  "tests": [
    {
      "test_id": "test_001",
      "name": "Creative Test Week 48",
      "platform": "facebook",
      "hypothesis": "Creative với CTA rõ ràng sẽ có CPL thấp hơn",
      "variant_a": {
        "description": "Creative A: Ảnh sản phẩm + CTA 'Đặt lịch tư vấn'"
      },
      "variant_b": {
        "description": "Creative B: Video UGC + CTA 'Xem kết quả'"
      },
      "primary_metric": "cpl",
      "start_date": "2026-03-10",
      "end_date": "2026-03-17",
      "min_sample": 50,
      "status": "running",
      "daily_data": [
        {
          "date": "2026-03-10",
          "variant_a": {
            "cost": 500000,
            "leads": 15,
            "clicks": 120,
            "impressions": 1200,
            "cpl": 33333.33,
            "cpc": 4166.67,
            "ctr": 10.0
          },
          "variant_b": {
            "cost": 480000,
            "leads": 18,
            "clicks": 130,
            "impressions": 1180,
            "cpl": 26666.67,
            "cpc": 3692.31,
            "ctr": 11.02
          }
        }
      ],
      "result": null
    }
  ],
  "completed": [
    {
      "test_id": "test_completed_001",
      "name": "Creative Test Week 47",
      "platform": "facebook",
      "winner": "variant_a",
      "confidence": 85,
      "improvement": "18%",
      "conclusion": "Creative A có CTR cao hơn 18% so với B",
      "recommendation": "Scale Creative A, pause Creative B từ hôm nay",
      "completed_date": "2026-03-03"
    }
  ]
}
```

### Trigger Conditions
- User gõ `/ab-new`, `/ab-update`, `/ab-status`, `/ab-history`
- Hoặc nói natural language: "test mới", "cập nhật test", "xem test nào đang chạy", "lịch sử test"
- Auto-trigger: mỗi ngày 19h check tests có kết thúc không → alert nếu có winner (kết hợp với lead-monitor/report-ads skill)

### Error Handling
- Test ID không tồn tại → "Test không tìm thấy, xem danh sách: /ab-status"
- Missing required fields → "Thiếu field: [field]. Yêu cầu: name, platform, hypothesis, variant_a, variant_b, primary_metric, start_date, end_date, min_sample"
- Invalid dates → "start_date phải <= end_date"
- Metric không hợp lệ → "Primary metric phải trong: cpl, ctr, cpc, cvr"

---

## Dependencies
- `message` tool: gửi alert Telegram khi có winner
- `persistent-memory` skill (optional): lưu insights từ test kết thúc
- `hands-framework` skill: logging + state management chuẩn
- File I/O: read/write `tests.json`

---

## Example Workflow
```
1. Anh: "/ab-new [input]"
   → Skill tạo test, trả test_id

2. Hằng ngày (~18h) anh update: "/ab-update test_001 [metrics]"
   → Skill tính CPL, check winner condition
   → Nếu đủ điều kiện: tự động gửi Telegram alert

3. Anh: "/ab-status"
   → Xem test nào đang chạy, tiến độ, hiệu suất hiện tại

4. Sau khi test kết thúc (auto-completed khi winner detected):
   → Anh: "/ab-history"
   → Xem kết quả + recommendation để scale/pause creative
```

---

## Notes
- Skill này **KHÔNG** fetch data trực tiếp từ FB Ads API / Google Ads API. Anh phải manual input hoặc script tự động pull data từ dashboard rồi gửi vào skill.
- Confidence score mặc định 85% (đơn giản). Nếu cần statistical rigor cao hơn (Chi-square, t-test), có thể extend sau.
- Mọi test mới tự động ghi log vào persistent-memory để anh có thể trace back.
