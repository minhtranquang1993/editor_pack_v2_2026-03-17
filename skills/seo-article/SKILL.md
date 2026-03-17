---
name: seo-article
description: >-
  Viết full SEO article chuẩn AEO/GEO/E-E-A-T cho keyword bất kỳ. Dùng khi
  anh nói "viết bài [keyword]", "/seo-content-full keyword=...", hoặc Writer Bot
  trong content-factory cần viết article. Hỗ trợ params đầy đủ: brand, sector,
  location, address, website, hotline, pricing_table, target_audience.
---

# SEO Article Skill

## Params

**Bắt buộc:**
- `keyword` — từ khóa chính
- `brand` — tên thương hiệu
- `sector` — lĩnh vực (vd: phẫu thuật mắt, vận chuyển nhà)
- `location` — khu vực địa lý
- `address` — địa chỉ đầy đủ
- `website` — domain website

**Khuyến nghị mạnh (hỏi anh nếu thiếu trước khi viết):**
- `hotline` → dùng trong CTA + LocalBusiness schema
- `pricing_table` → bảng giá → tăng conversion
- `target_audience` → điều chỉnh tone, pain points, ví dụ

**Nếu thiếu params khuyến nghị:** note rõ assumption và ưu tiên hỏi anh trước khi publish.

---

## Chuẩn viết 2025–2026: SEO + AEO + GEO

### 1. Direct Answer Block (AEO — đầu bài)
Ngay sau H1, trước H2 đầu tiên: 2–3 câu trả lời thẳng vào keyword.
AI snippet / featured snippet sẽ lấy đoạn này.

```html
<!-- Direct answer — AEO snippet target -->
<p class="direct-answer">
  [Keyword] là... [định nghĩa ngắn gọn 1–2 câu].
  [Fact quan trọng nhất người dùng cần biết ngay].
</p>
```

### 2. Heading dạng câu hỏi (AEO)
- H2 viết như câu hỏi thực tế: "X là gì?", "Tại sao Y?", "Có nên Z không?"
- H3 granular: "Chi phí X tại [location] là bao nhiêu?", "X có nguy hiểm không?"
- Mỗi H2 section mở đầu = direct answer 1–2 câu trước khi đi vào chi tiết

### 3. E-E-A-T Signals
- Có **brand mention** tự nhiên ít nhất 3 lần trong body
- Có **địa chỉ + location** trong body (không chỉ ở CTA)
- Có **dẫn chứng / số liệu** cụ thể (%, năm, case study)
- Có **author context** nếu cần (bác sĩ, chuyên gia)

### 4. GEO — Third-party & AI Citation Signals
- Đề cập đến các nguồn uy tín trong ngành (WHO, Bộ Y Tế, hiệp hội...)
- Viết content **factual, verifiable** — AI dễ cite
- **Niche content**: viết cụ thể cho đúng đối tượng, đúng địa phương
- Tránh broad/generic → AI prefer specific answers

### 5. FAQ Section (AEO + GEO)
Bắt buộc có mục FAQ cuối bài — 3–5 câu hỏi thực tế từ People Also Ask.
Format chuẩn để AI trích dẫn:

```html
<section class="faq">
  <h2>Câu Hỏi Thường Gặp</h2>
  <div class="faq-item">
    <h3>[Câu hỏi cụ thể?]</h3>
    <p>[Trả lời direct, 2–4 câu]</p>
  </div>
  <!-- repeat -->
</section>
```

---

## HTML Output Template

```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>{keyword} | {brand}</title>
  <meta name="description" content="{meta_desc — 150-160 ký tự, có keyword + brand}">
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "LocalBusiness",
    "name": "{brand}",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "{address}",
      "addressLocality": "{location}",
      "addressCountry": "VN"
    },
    "telephone": "{hotline}",
    "url": "https://{website}"
  }
  </script>
  <!-- FAQ Schema nếu có FAQ section -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {
        "@type": "Question",
        "name": "{câu hỏi 1}",
        "acceptedAnswer": {
          "@type": "Answer",
          "text": "{trả lời 1}"
        }
      }
    ]
  }
  </script>
</head>
<body>

  <h1>{H1 — dạng câu hỏi hoặc benefit, có keyword chính}</h1>

  <!-- Direct Answer Block — AEO snippet target -->
  <p class="direct-answer">{Trả lời thẳng keyword trong 2–3 câu}</p>

  <!-- Body content theo outline -->
  <h2>{H2 dạng câu hỏi}</h2>
  <p>{Direct answer 1–2 câu}</p>
  <!-- chi tiết section -->

  <!-- Pricing table nếu có pricing_table param -->
  <h2>Bảng Giá {sector} Tại {brand}</h2>
  <table>
    <!-- {pricing_table} -->
  </table>

  <!-- FAQ Section — bắt buộc -->
  <section class="faq">
    <h2>Câu Hỏi Thường Gặp Về {keyword}</h2>
    <!-- 3–5 Q&A -->
  </section>

  <!-- CTA cuối bài — bắt buộc -->
  <section class="cta">
    <h2>Liên Hệ {brand}</h2>
    <p>📍 {address}</p>
    <p>🌐 {website}</p>
    <p>📞 {hotline}</p>
  </section>

</body>
</html>
```

---

## Research/Facts process (trước khi viết)

1. Dùng `search-kit` để lấy nguồn mới nhất cho keyword
   - Fast lookup: `python3 skills/search-kit/scripts/search_router.py --query "{keyword}" --mode fast --json`
   - Deep research (SEO/competitor): `python3 skills/search-kit/scripts/search_router.py --query "{keyword}" --mode pro --json`
2. Extract 3–5 URLs chất lượng để làm nguồn factual
3. Chỉ đưa số liệu có nguồn; nếu không chắc thì viết mức tham khảo, không khẳng định tuyệt đối
4. Nếu nguồn mâu thuẫn: chạy lại mode `pro`, đối chiếu thêm nguồn thứ 2

## 🧠 Anti-Hallucination Rules (BẮT BUỘC)

### Trước khi viết
- **Mọi số liệu (%, giá, năm, case study)** phải đến từ research output (search-kit). KHÔNG bịa số
- Không tìm được số liệu → viết dạng mô tả ("chi phí hợp lý", "tỷ lệ thành công cao") thay vì bịa con số cụ thể
- Nguồn uy tín (WHO, Bộ Y Tế...) → verify link tồn tại trước khi cite. KHÔNG tạo link giả

### Trong khi viết
- Mỗi claim có số liệu → kèm nguồn hoặc ghi rõ "theo [nguồn]"
- KHÔNG viết: "theo nghiên cứu năm 20XX" nếu không có nghiên cứu thật
- KHÔNG bịa tên bác sĩ, tên bệnh viện, giải thưởng không có thật
- Pricing table → chỉ điền khi có `pricing_table` param. Không có → bỏ trống hoặc ghi "Liên hệ"
- KHÔNG dùng từ tuyệt đối nếu thiếu chứng cứ: "tốt nhất", "duy nhất", "100%", "cam kết khỏi hoàn toàn"

### Sau khi viết (self-check)
- [ ] Scan toàn bài: có số nào em "cảm thấy đúng" nhưng không từ research? → Xóa hoặc verify
- [ ] Có URL nào chưa fetch? → Fetch thử hoặc xóa
- [ ] Có claim nào quá tuyệt đối ("tốt nhất", "duy nhất", "100%")? → Soften hoặc cite nguồn

---

## Checklist trước khi deliver

- [ ] **🧠 Anti-hallucination check passed** (số liệu có nguồn, link valid, không bịa)
- [ ] Direct answer block ngay sau H1
- [ ] H2/H3 dạng câu hỏi (≥ 60% headings)
- [ ] Brand mention tự nhiên ≥ 3 lần
- [ ] Location + address trong body (không chỉ CTA)
- [ ] Số liệu / dẫn chứng cụ thể ≥ 2 chỗ **(có nguồn)**
- [ ] FAQ section có ≥ 3 Q&A
- [ ] FAQ Schema JSON-LD
- [ ] LocalBusiness Schema JSON-LD (khi có hotline/address)
- [ ] Pricing table (nếu có `pricing_table`)
- [ ] Tone khớp `target_audience` (nếu có)
- [ ] CTA cuối bài đầy đủ hotline/địa chỉ/website
- [ ] Word count 2000–2500 từ (mặc định)
- [ ] Meta description 150–160 ký tự, có keyword + brand

---

## Word count per section (default)
- Intro + direct answer: ~150 từ
- Mỗi H2 section: 200–350 từ
- FAQ: ~200 từ
- CTA: ~100 từ
- Tổng: ~2000–2500 từ

## Output Contract (Tier-2)

**Output bắt buộc:**
- Title + slug + excerpt
- Phần mở đầu trả lời trực tiếp (AEO direct answer)
- Nội dung theo outline, có CTA rõ
- FAQ section
- SEO meta: meta title + meta description + tags đề xuất

**Definition of Done:**
- Bài hoàn chỉnh publish-ready (không phải draft rời rạc)
- Logic mạch lạc, đúng keyword intent
- Có đủ metadata để đăng web/CMS

## Category
content-seo

## Trigger

Use this skill when:
- Cần viết bài SEO hoàn chỉnh
- Tạo content chuẩn SEO với HTML
- User says: "viết bài SEO", "viết content", "/seo-content", "bài viết SEO"