---
name: seo-outline
description: >-
  Tạo SEO outline chuẩn AEO/GEO cho bất kỳ keyword nào. Dùng khi anh nói
  "viết outline [keyword]", "lên outline", "tạo dàn bài SEO". Hỗ trợ 3 mức độ
  outline (lite/standard/deep) để tránh quá dài: mặc định lite.
---

# SEO Outline Skill

> ⚠️ **MANDATORY WORKFLOW — KHÔNG ĐƯỢC BỎ QUA:**
> 1. Research → 2. Tạo outline → 3. **BẮT BUỘC review ngay lập tức**
> Chưa có review = chưa xong task. Không đợi anh nhắc.
> ❌ KHÔNG review trước khi có outline — phải chờ outline xong mới review.

## Input

| Param | Bắt buộc | Mô tả |
|---|---|---|
| `keyword` | ✅ | Từ khóa chính |
| `mode` | ❌ | `lite` \| `standard` \| `deep` (mặc định: `lite` để tránh dài) |

Ví dụ trigger:
- `/seo-outline keyword="mắt cận thị khi về già"`
- `/seo-outline keyword="các loại lens cận" mode=lite`
- `viết outline deep cho keyword ...`

---

## Output Contract (chuẩn duy nhất — bắt buộc tuân thủ)

**Output bắt buộc, theo đúng thứ tự này:**

```text
Keyword chính: {keyword}
Intent: {informational | commercial | transactional | navigational} [local | non-local]

H1: {title — dạng câu hỏi hoặc benefit-driven}
H2: {section}
H3: {subsection}
H3: {subsection} [cần dẫn chứng]
H2: {section}
...
H2: FAQ
H3: {câu hỏi 1}
H3: {câu hỏi 2}
...

AIO Notes:
- Entity definitions: {thuật ngữ 1}, {thuật ngữ 2}, {thuật ngữ 3}
- Decision factors: {tiêu chí 1}, {tiêu chí 2}, {tiêu chí 3}

SEO Meta:
- Slug: {slug-lowercase-khong-dau-dung-gach-ngang} (rule: lowercase, `-` thay khoảng trắng, bỏ ký tự đặc biệt, bỏ stopword thừa như "va"/"cua"/"la")
- Meta title: {<60 ký tự, có keyword}
- Meta description: {120–155 ký tự, có keyword + CTA nhẹ}

Tham khảo bài viết:
https://...
https://...
https://...
```

**Rules:**
- Không thêm intro, outro, ghi chú, giải thích ngoài format trên
- Không đánh số thứ tự trước H2/H3
- Tag `[cần dẫn chứng]` phải inline sau heading nào cần số liệu/nghiên cứu/chuyên gia
- `AIO Notes` là block cố định — **không được bỏ qua**
- Cuối bắt buộc có `Tham khảo bài viết:` + 3–5 URLs thực tế đã dùng để research

---

## Length Control (anti-overlong)

### 1) Mode budget

> **Định nghĩa:** "H3 tổng" = tổng tất cả H3 trong bài, **bao gồm cả FAQ H3**. FAQ H3 là subset của H3 tổng, không được đếm thêm.

| Mode | H2 | H3 tổng (gồm FAQ) | FAQ H3 | Dùng khi |
|---|---:|---:|---:|---|
| `lite` (default) | 4–6 | 6–12 | 2–3 | Q&A ngắn, intent hẹp, cần viết nhanh |
| `standard` | 6–8 | 12–20 | 3–5 | Cần độ sâu hơn mặt bằng bài đối thủ |
| `deep` | 8–12 | 20–36 | 5–8 | Pillar/tổng hợp lớn, cạnh tranh cao |

### 2) Auto mode (khi user không chỉ định)
- Keyword dạng **Q&A hẹp**: "là gì / có ... không / nên ... không" → `lite` hoặc `standard`
- Keyword dạng **tổng hợp rộng**: "các loại / hướng dẫn toàn diện / so sánh chi tiết" → `deep`
- Không chắc chắn → chọn `lite` (ưu tiên gọn giống mặt bằng đối thủ)

### 3) Hard caps chống lan man
- Mỗi H2 chỉ **1 intent**
- `lite`: mỗi H2 tối đa **1–2 H3**
- `standard`: mỗi H2 tối đa **2–3 H3**
- `deep`: mỗi H2 tối đa **3–4 H3**
- Nếu 2 H2 trùng intent → gộp lại
- Ưu tiên bám mặt bằng đối thủ: nếu competitor coverage đã đủ ngắn/gọn thì KHÔNG tự mở rộng thêm chỉ để "cho đủ SEO"

---

## AEO/GEO Heading Rules (2025–2026)

### H1
- Ưu tiên dạng câu hỏi: "X là gì?", "Tại sao Y?", "Có nên Z không?"
- Hoặc benefit-driven: "Cách X hiệu quả nhất tại [location]"
- Có keyword chính tự nhiên

### H2
- Viết như câu hỏi người dùng thật sự search
- Mỗi H2 = 1 intent rõ ràng (định nghĩa / nguyên nhân / cách làm / so sánh / FAQ...)
- Trả lời được dạng AI snippet / featured snippet

### H3
- Cụ thể, granular — AI dùng H3 để trích dẫn niche queries
- Không vague: ❌ "Thông tin thêm" ✅ "Chi phí phẫu thuật LASIK tại TP.HCM là bao nhiêu?"

---

## Cấu trúc outline chuẩn (theo search intent)

### Informational (phổ biến nhất — y tế, giáo dục, tư vấn)
```text
H2: [Keyword] là gì?
H3: Định nghĩa
H3: Phân loại / Các dạng
H2: Nguyên nhân / Dấu hiệu
H3: (cụ thể từng nguyên nhân)
H2: Cách nhận biết / Chẩn đoán
H2: Phương pháp xử lý / Điều trị
H3: (từng phương pháp) [cần dẫn chứng]
H2: Khi nào nên gặp chuyên gia?
H2: FAQ (theo mode: 2–3 lite / 3–5 standard / 5–8 deep)
H2: [Brand] — Dịch vụ liên quan (nếu có)
```

### Commercial / Local (dịch vụ, phòng khám, chuyển nhà...)
```text
H2: [Dịch vụ] là gì? / [Dịch vụ] bao gồm những gì?
H2: Lợi ích / Tại sao cần [dịch vụ]?
H2: Quy trình thực hiện
H2: Bảng giá / Chi phí tham khảo tại [khu vực] [cần dẫn chứng]
H2: Tiêu chí chọn đơn vị uy tín
H2: [Brand] — Tại sao chọn chúng tôi?
H2: FAQ (theo mode)
```

---

## Research process trước khi viết outline

1. Fetch top 3–5 kết quả cho keyword bằng `search-kit` (ưu tiên)
- Nhanh: `python3 skills/search-kit/scripts/search_router.py --query "{keyword}" --mode fast --json`
- Cần sâu (SEO/đối thủ): `python3 skills/search-kit/scripts/search_router.py --query "{keyword}" --mode pro --json`
- Nếu cần crawl nội dung sạch từng URL: dùng thêm `reader-adapter`
2. Xác định **primary intent** (informational / commercial / transactional / navigational) và **modifier** (local / non-local)
3. **Phân tích SERP feature** — xác định format top SERP đang thiên về dạng nào:
- Listicle/list → ưu tiên H2/H3 dạng list items
- Comparison/bảng tiêu chí → bắt buộc có H2 so sánh + bảng
- Pricing → bắt buộc có section bảng giá
- How-to/step-by-step → ưu tiên flow từng bước
- Local pack → kích hoạt GEO local block
4. **Ưu tiên học top 1–3**: extract cấu trúc H2/H3 và pattern section (thứ tự ý, mức độ chi tiết)
5. Xác định **median competitor depth**: số H2/H3 trung vị trong top 1–3
6. Tạo outline theo mode budget (xem bảng ở trên)
7. Map thêm related queries (People Also Ask) → chỉ chọn câu thật sự liên quan
8. Lưu 3–5 URLs làm "Tham khảo bài viết"

---

## AIO Signals (bắt buộc in trong output — xem Output Contract)

Mỗi outline phải in block `AIO Notes:` với 2 mục:
- **Entity definitions:** 3–5 thuật ngữ chính/phụ mà writer cần định nghĩa rõ trong bài
- **Decision factors:** 2–4 tiêu chí reader dùng để ra quyết định (mua/chọn/làm)

Ngoài ra, các H2/H3 nào cần số liệu, nghiên cứu hoặc trích dẫn chuyên gia → gắn tag `[cần dẫn chứng]` inline ngay sau heading đó trong outline.

---

## GEO Signals (bắt buộc khi modifier = local)

Khi intent modifier là `local` → **bắt buộc thêm Local Intent Block** vào outline:

```text
H2: [Dịch vụ] tại [khu vực] — Thông tin địa phương
H3: Khu vực phục vụ (quận/huyện cụ thể)
H3: Mức giá tham khảo tại [thành phố] [cần dẫn chứng]
H3: FAQ địa phương (câu hỏi theo địa điểm)
H3: CTA địa phương ("Đặt lịch tại [địa chỉ]", "Hotline khu vực...")
```

Nếu modifier = `non-local` → bỏ qua block này.

---

## E-E-A-T / Trust Signals (bắt buộc với YMYL)

**YMYL topics** (y tế, tài chính, pháp lý, an toàn) → outline **bắt buộc có ít nhất 1** trong các block sau:

| Block | Ví dụ heading |
|---|---|
| Khi nào cần chuyên gia | "Khi nào cần gặp bác sĩ thay vì tự điều trị?" |
| Tiêu chí an toàn / rủi ro | "Những rủi ro nào cần biết trước khi thực hiện?" |
| Cơ sở pháp lý / chuẩn chuyên môn | "Theo quy định của Bộ Y tế / chuẩn quốc tế..." |
| Cảnh báo tự xử lý | "Trường hợp nào KHÔNG nên tự xử lý tại nhà?" |

Nếu không phải YMYL → không bắt buộc, nhưng vẫn được khuyến khích nếu phù hợp.

---

## Auto-Review Workflow (Bắt buộc)

Sau khi tạo xong outline, **BẮT BUỘC** tự động review và chấm điểm ngay (không đợi anh nhắc).

**Quy tắc thực hiện Review:**
1. **Model ưu tiên:** Thực hiện bằng model `minai93/gemini-3.1-pro-high` (alias: `gemini31`) qua tool `sessions_spawn`.
- Nếu `sessions_spawn` hoặc `gemini31` **không khả dụng** → fallback: dùng model hiện tại thực hiện review ngay, gắn cờ `[review degraded mode]` ở đầu phần review.
- ❌ Không được bỏ qua review vì thiếu tool/model — luôn có fallback.
2. **Format phần Review** (giới hạn ngắn — không được dài hơn):
- **Điểm số:** Chấm trên thang điểm 10.
- **Lý do:** Tối đa 3 bullet — phân tích Search Intent, AEO/SEO snippet readiness, tính chuyển đổi.
- **Gợi ý 10/10:** 1–2 điểm cụ thể để outline hoàn hảo hơn. Không giải thích dài.

---

## QA Checklist (pass/fail trước khi trả outline)

| # | Tiêu chí | Pass nếu... |
|---|---|---|
| 1 | Mode budget | Số H2/H3/FAQ đúng với mode đã chọn |
| 2 | Không trùng intent H2 | Mỗi H2 = 1 intent khác nhau |
| 3 | Không H2/H3 mơ hồ | Tất cả heading đủ cụ thể, không vague |
| 4 | Có nguồn thật | Có ≥3 URLs thực tế từ research |
| 5 | Đủ block bắt buộc | Intent (primary+modifier), H1, H2/H3, FAQ, AIO Notes, SEO Meta, Nguồn |
| 6 | AIO signals in ra | Block `AIO Notes:` có Entity definitions + Decision factors |
| 7 | Evidence tags | Các H2/H3 cần dẫn chứng đã gắn `[cần dẫn chứng]` |
| 8 | GEO block | Có Local Intent Block nếu modifier = local |
| 9 | E-E-A-T block | Có ≥1 trust block nếu là YMYL topic |
| 10 | SEO meta đầy đủ | Slug + Meta title (<60 ký tự) + Meta description (120–155 ký tự) |

**Nếu bất kỳ tiêu chí nào FAIL → sửa trước khi trả outline.**

## Category
content-seo
