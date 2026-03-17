---
name: analyze-mess-ads
description: Analyze Messenger ads content performance by group (doctor/UGC/promo) using ad metrics + lead status funnel. Use when asked to compare messaging efficiency, CPL quality, and conversion quality by creative theme.
---

# Analyze Messenger Ads — Content Performance

> Phân tích hiệu quả content ads trên Messenger theo nhóm nội dung.
> Trigger: "analyze ads mess", "phân tích ads mess", "analyze messenger ads"

## Data Sources

1. **Facebook Ads API** — ad-level insights (campaign filter: `_DNDA_MS_`)
2. **Supabase DND** — leads data (platform_ads = Messenger)

## Content Groups (phân theo ad_name / campaign_name)

| Nhóm | Filter | Điều kiện |
|---|---|---|
| Bác sĩ Tuấn | ad_name chứa `Bacsi.Tuan` | case-insensitive |
| Bác sĩ Hà | ad_name chứa `Bacsi.Ha` | case-insensitive |
| UGC | ad_name chứa `VID_UGC` hoặc `UGC` | case-insensitive |
| CTKM | ad_name hoặc campaign_name chứa `IMG.CTKM` | case-insensitive |

> Nếu anh thêm nhóm mới → update bảng này.

## Metrics per Group

| Metric | Nguồn | Cách tính |
|---|---|---|
| Mess (tin nhắn) | FB API `onsite_conversion.messaging_first_reply` | Tổng per group |
| CP Mess | FB API | cost / mess |
| Lead tổng | Supabase `data` table | Count per group |
| CPL | FB API + Supabase | cost / lead |
| Lead quan tâm | Supabase status = `dat_lich` hoặc `da_kham` | Count |
| % Quan tâm | Supabase | quan_tam / total * 100 |
| Lead đã khám | Supabase status = `da_kham` | Count |
| % Đã khám | Supabase | da_kham / total * 100 |

## Workflow

```
1. FB Ads API → fetch ad-level insights (filter _DNDA_MS_)
   - fields: ad_name, campaign_name, spend, actions
   - level: ad
   - time_range: 30 ngày (default) hoặc theo yêu cầu
   - paginate until hết data

2. Supabase → fetch leads (filter Messenger + _DNDA_MS_)
   - table: data
   - filter: platform_ads=Messenger, campaign_name like *_DNDA_MS_*
   - fields: ad_name, campaign_name, status

3. Classify → map mỗi ad/lead vào 4 groups

4. Calculate → tính metrics per group

5. Report → gửi Telegram theo template
```

## Report Template (Telegram)

```
📊 *PHÂN TÍCH CONTENT ADS — MESSENGER*
📅 {period}
🔍 Filter: campaign `_DNDA_MS_`

{per_group}:
▸ *{group_name}*
  💬 Mess: *{msgs}* | CP Mess: {cp_mess}
  🎯 Lead: *{leads}* | CPL: {cpl}
  ⭐ Quan tâm: *{qt}* ({pct_qt}%) | Đã khám: *{dk}* ({pct_dk}%)
  💰 Chi phí: {cost}

━━━━━━━━━━━━━━━━━━━━━
📌 *TỔNG KẾT*
💰 Tổng chi: *{total_cost}*
💬 Tổng mess: *{total_msgs}* | CP Mess TB: {avg_cp_mess}
🎯 Tổng lead: *{total_leads}* | CPL TB: {avg_cpl}
⭐ Quan tâm: *{total_qt}* ({pct_qt_total}%)
✅ Đã khám: *{total_dk}* ({pct_dk_total}%)

💡 *Insight nhanh:*
{auto_insights}
```

## Drill-down (khi anh hỏi chi tiết 1 nhóm)

List từng ad_name trong nhóm đó:
```
🎬 *{group} — CHI TIẾT TỪNG AD NAME*

*1️⃣ {ad_name}* {star_if_best}
💬 Mess: *{msgs}* | CP Mess: {cp_mess}
🎯 Lead: *{leads}* | Quan tâm: *{qt}* | Đã khám: *{dk}*
💰 Chi phí: {cost}
→ {comment}
```

## Auto Insights Logic

- CP Mess thấp nhất → highlight "chi phí per mess tốt nhất"
- % Đã khám cao nhất → highlight "chuyển đổi tốt nhất"
- 0 lead hoặc 0 mess → flag "cần review content"
- CPL > 5tr → flag "CPL cao"

## Config

- Default period: 30 ngày
- Anh có thể chỉ định: "analyze ads mess 7 ngày", "analyze ads mess tháng 1"
- **KHÔNG sửa code website data ads** — chỉ đọc API + DB

## Mesh Connections
- **← report-ads**: Có thể gọi sau report daily để deep dive
- **→ search-kit**: Benchmark CPL ngành nếu cần so sánh

## Output Contract (Tier-2)

**Output bắt buộc:**
- Bảng theo nhóm content: Mess, CP Mess, Leads, CPL, %Quan tâm, %Đã khám
- Nhóm tốt nhất và kém nhất
- 3 khuyến nghị tối ưu cụ thể

**Definition of Done:**
- So sánh được hiệu quả giữa các nhóm
- Có khuyến nghị hành động (không chỉ mô tả số liệu)

## Category
marketing-ads
