---
name: search-kit
description: Multi-engine web search router for research tasks. Use when cần tra cứu thông tin web, research SEO, phân tích đối thủ, fact-check, hoặc khi user nói "search", "nghiên cứu", "tìm nguồn". Ưu tiên Perplexity (Sonar/Sonar Pro với budget $5/tháng), tự fallback sang Tavily → SerpAPI → Google CSE → SearXNG khi hết budget hoặc lỗi.
---

# Search Kit

## Mục tiêu
- Tra cứu web nhanh, có nguồn, tối ưu chi phí.
- Mặc định dùng Perplexity theo policy 80/20:
  - 80% `sonar` (fast)
  - 20% `sonar-pro` (deep research)
- Khi Perplexity hết budget hoặc lỗi: fallback sang engine khác.

## Cách dùng nhanh

```bash
# Auto route (khuyến nghị)
python3 skills/search-kit/scripts/search_router.py --query "..."

# Fast lookup
python3 skills/search-kit/scripts/search_router.py --query "..." --mode fast

# Deep SEO/competitor research
python3 skills/search-kit/scripts/search_router.py --query "..." --mode pro

# Xem budget Perplexity
python3 tools/perplexity_search.py --status
```

## Quy tắc chọn mode
- `fast` → tra cứu nhanh, hỏi đáp thường, cần tốc độ.
- `pro` → SEO research, competitor analysis, chủ đề cần độ sâu.
- `auto` → ưu tiên bám tỷ lệ 80/20 trong `tools/perplexity_search.py`.

## Fallback order
1. Perplexity (`tools/perplexity_search.py`)
2. Tavily
3. SerpAPI
4. Google CSE
5. SearXNG (nếu cấu hình URL)

## Output
Router trả JSON gồm:
- `engine`
- `model` (nếu có)
- `content`/`items`
- `sources`
- `fallback_used`
- `quality_score`
- `quality_status`

## Quality Gate
- Mặc định có quality threshold `0.6`
- Kết quả Perplexity chất lượng thấp sẽ tự retry 1 lần với `--mode pro`
- Fallback engines nếu chất lượng thấp sẽ bị skip để thử engine tiếp theo
- Có thể override bằng `--quality-threshold 0.0` để tắt quality check khi cần backward compatibility

## Notes
- Secrets/API keys ưu tiên đọc từ `.env`.
- Nếu kết quả mâu thuẫn nguồn: chạy lại với `--mode pro` rồi đối chiếu thêm nguồn.
- Nếu tất cả engines fail: báo rõ fail + dùng `web_search` tool để cứu hộ thủ công.

## Category
automation

## Trigger

Use this skill when:
- Cần tìm kiếm thông tin trên web
- Research một chủ đề cụ thể
- User says: "search", "tìm kiếm", "research", "nghiên cứu", "tìm thông tin"