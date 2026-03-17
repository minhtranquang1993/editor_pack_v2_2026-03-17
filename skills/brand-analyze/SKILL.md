---
name: brand-analyze
description: >-
  Phân tích toàn diện 1 brand/website: sản phẩm, đối tượng, target audience, đối thủ, SWOT...
  Trigger: "/brand-analyze [URL hoặc tên brand]", "phân tích brand", "phân tích website", "phân tích thương hiệu", "analyze brand"
---

# 📋 SKILL: /brand-analyze

## Input

| Param | Bắt buộc | Mô tả |
|-------|----------|-------|
| **URL hoặc tên brand** | ✅ Bắt buộc | URL website (ưu tiên) hoặc tên brand (em tự search tìm website) |
| **Mục đích** | ⭐ Nên có | Phân tích để làm gì? (viết content, tìm gap cạnh tranh, pitch KH mới, học hỏi marketing...) → em sẽ đào sâu phần liên quan |
| **Ngành** | 💡 Optional | Chỉ cần khi brand đa ngành, em không tự nhận ra |

**Đối thủ, thị trường, audience → em TỰ tìm ra. Đó là việc của em, không phải anh cung cấp.**

Ví dụ:
```
/brand-analyze https://matquoctednd.vn
→ mục đích: hiểu audience để viết content ads

/brand-analyze Thế Giới Di Động
→ (không cần thêm gì, em tự research)
```

## Output — 11 mục phân tích

| # | Mục | Nội dung |
|---|-----|----------|
| 1 | **Brand Overview** | Tên, ngành, slogan, quy mô, năm thành lập |
| 2 | **Products & Services** | Danh sách SP/DV chính, pricing model, USP |
| 3 | **Pricing Position** | Phân khúc giá (budget/mid/premium/luxury), so sánh thị trường |
| 4 | **Target Audience & Persona** | Demographics, 1-2 chân dung KH, pain points |
| 5 | **Marketing & Channels** | Tone/voice, kênh marketing, CTA chính, funnel, customer journey |
| 6 | **Content Strategy** | Blog/social, tần suất, chủ đề chính |
| 7 | **Trust Signals** | Reviews, chứng nhận, báo chí, đối tác, KOL |
| 8 | **Brand Perception** | Từ khóa KH hay dùng khi nói về brand |
| 9 | **Competitor Snapshot** | 2-3 đối thủ chính + so sánh nhanh |
| 10 | **SWOT** | Strengths / Weaknesses / Opportunities / Threats |
| 11 | **Weakness & Gaps** | Lỗ hổng brand đang bỏ ngỏ, cơ hội khai thác |

## ⚠️ QUY TẮC CHỐNG HALLUCINATION (BẮT BUỘC)

1. **CHỈ phân tích từ dữ liệu đã crawl/search thật** — KHÔNG bịa thông tin
2. Nếu không tìm thấy dữ liệu cho mục nào → ghi rõ: `[Không tìm thấy dữ liệu]`
3. **KHÔNG đoán** số liệu (follower, traffic, doanh thu) nếu không có nguồn
4. Mỗi insight quan trọng phải có **source** (URL hoặc trang đã crawl)
5. Phân biệt rõ: **Dữ liệu thực** vs **Nhận định phân tích** (đánh dấu nhận định bằng 💡)
6. Nếu brand quá mới / ít thông tin → báo anh, không cố bịa cho đủ 11 mục

## Workflow

```
/brand-analyze <URL hoặc tên brand>
  │
  ├─ Phase 1: Thu thập dữ liệu (SUB agents - haiku, song song)
  │   ├─ SUB 1: Crawl website chính (reader-adapter)
  │   │   └─ Trang chủ + About + Services/Products + Blog (max 5-8 trang)
  │   ├─ SUB 2: Search thông tin bổ sung (search-kit / web_search)
  │   │   └─ "[brand] reviews", "[brand] đối thủ", "[brand] tin tức"
  │   └─ SUB 3: Check social presence (web_fetch)
  │       └─ FB page, LinkedIn, TikTok (nếu tìm thấy link)
  │
  ├─ Phase 2: Phân tích & tổng hợp (MAIN - sonnet)
  │   └─ Đọc tất cả dữ liệu crawl/search → phân tích 11 mục
  │   └─ Đánh dấu rõ: dữ liệu thực vs nhận định phân tích
  │
  └─ Phase 3: Output report
      └─ Telegram message (structured, có emoji)
      └─ Nếu anh cần: lưu file markdown chi tiết
```

### Chi tiết Phase 1 — Thu thập dữ liệu

**Crawl website (reader-adapter):**
```bash
# Crawl max 8 trang, depth 2
python3 tools/reader_tools.py crawl --url "<website>" --depth 2 --max-pages 8 --scrape --standalone
```

**Search bổ sung (web_search hoặc search-kit):**
- Query 1: `"[brand name]" reviews đánh giá`
- Query 2: `"[brand name]" đối thủ competitors`
- Query 3: `"[brand name]" tin tức news 2024 2025`

**Check social (web_fetch nhanh):**
- Tìm link social từ website đã crawl → fetch nhanh để check follower/activity

### Chi tiết Phase 2 — Prompt phân tích

Khi phân tích, em PHẢI follow template này:

```
Dựa HOÀN TOÀN vào dữ liệu đã thu thập bên dưới, phân tích brand theo 11 mục.

QUY TẮC:
- CHỈ dùng thông tin có trong dữ liệu. KHÔNG bịa.
- Không có dữ liệu → ghi "[Không tìm thấy dữ liệu]"
- Đánh dấu nhận định phân tích bằng 💡
- Dữ liệu thực ghi nguồn

[DỮ LIỆU CRAWL]
...

[DỮ LIỆU SEARCH]
...
```

## Output Format (Telegram)

```
🏢 BRAND ANALYSIS: [Tên Brand]
🔗 [URL]
📅 Phân tích ngày: [date]

━━━━━━━━━━━━━━━━━━━━

1️⃣ BRAND OVERVIEW
...

2️⃣ PRODUCTS & SERVICES
...

3️⃣ PRICING POSITION
...

4️⃣ TARGET AUDIENCE & PERSONA
...

5️⃣ MARKETING & CHANNELS
...

6️⃣ CONTENT STRATEGY
...

7️⃣ TRUST SIGNALS
...

8️⃣ BRAND PERCEPTION
...

9️⃣ COMPETITOR SNAPSHOT
...

🔟 SWOT
...

1️⃣1️⃣ WEAKNESS & GAPS
...

━━━━━━━━━━━━━━━━━━━━
📌 Sources: [danh sách URL đã dùng]
💡 = Nhận định phân tích (không phải dữ liệu trực tiếp)
```

## Notes
- Task > 3 bước → delegate cho sub-agents (Phase 1 song song)
- Observation masking: nếu crawl output > 200 dòng → tóm tắt key info, không dump raw
- Budget: ~3-5 web_search calls + 1 crawl + vài web_fetch = chi phí thấp
- Thời gian ước tính: 2-4 phút

## Mesh Connections
- **← reader-adapter**: crawl website chính
- **← search-kit**: search thông tin bổ sung, đối thủ, reviews
- **→ seo-article**: dùng brand analysis làm input cho viết content
- **→ copywriting**: dùng audience/persona để viết copy chuẩn target
- **→ content-factory**: brand analysis là bước đầu trong pipeline content

## Output Contract (Tier-2)

**Output bắt buộc:**
- Snapshot brand: định vị, sản phẩm/dịch vụ, tệp khách hàng
- Competitor set (ít nhất 3)
- SWOT
- Gap chính + kế hoạch hành động 14 ngày

**Definition of Done:**
- Có insight dùng được cho marketing action
- Không chỉ lý thuyết chung, phải có bước triển khai cụ thể

## Category
content-seo
