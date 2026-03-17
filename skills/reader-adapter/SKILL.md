---
name: reader-adapter
description: >-
  Production-grade web scraping/crawling adapter using vakra-dev/reader CLI.
  Use when tasks need robust scrape/crawl with markdown output, batch concurrency,
  retries/timeouts, and cleaner content extraction than basic fetch.
---

# Reader Adapter

## What this skill does

- Uses `reader` (vakra-dev/reader) for robust web scraping/crawling
- Outputs structured JSON + clean markdown for downstream RAG/research
- Supports daemon mode for warm browser pool on repeated jobs

## Commands

### Scrape one URL
```bash
python3 tools/reader_tools.py scrape --url "https://example.com" --standalone
```

### Crawl site
```bash
python3 tools/reader_tools.py crawl --url "https://example.com" --depth 2 --max-pages 20 --scrape --standalone
```

### Daemon mode (for repeated/batch workloads)
```bash
python3 tools/reader_tools.py start --pool-size 3
python3 tools/reader_tools.py status
python3 tools/reader_tools.py stop
```

## Output locations

- `memory/reader/scrape_*.json`
- `memory/reader/crawl_*.json`

## Integration guidance

- For `search-kit`/`rag-kit`: scrape source URL then ingest markdown
- For deep research: crawl domain, then summarize pages with haiku/sonnet
- Prefer `--standalone` for one-off runs; use daemon for many URLs

## Decision note (2026-02-22)

- Đã benchmark nhanh crawler hiện tại (`reader`) trên 3 URL: pass ổn định, tốc độ tốt, markdown sạch.
- Đã thử cài `crawl4ai` trong sandbox nhưng fail dependency build (`lxml` wheel), chưa crawl benchmark được.
- Quyết định hiện tại: giữ `reader-adapter` làm crawler mặc định; chỉ quay lại thử `crawl4ai` khi có nhu cầu case khó (JS nặng/chống bot/crawl sâu).

## Category
automation

## Trigger

Use this skill when:
- Cần scrape/crawl nội dung từ web
- Batch fetch nhiều URL cùng lúc
- User says: "scrape web", "crawl URL", "batch fetch", "đọc nội dung web"