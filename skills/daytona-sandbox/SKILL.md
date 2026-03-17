---
name: daytona-sandbox
description: >-
  Secure isolated sandbox via Daytona API. Dùng khi cần: chạy code untrusted,
  web scraping/Playwright không lo block IP, xử lý file nặng (CSV/PDF/image),
  test scripts trước production, SEO content pipeline chạy song song.
  Sandbox spin up <90ms, tự cleanup sau khi xong.
---

# 📋 SKILL: Daytona Sandbox
# Location: /root/.openclaw/workspace/skills/daytona-sandbox/

## Mô tả

Chạy code/scripts trong sandbox isolated — không ảnh hưởng VPS chính.
IP sandbox sạch (US datacenter), Python 3.14, pre-installed nhiều packages.

---

## Config

```python
API_KEY = "dtn_9a594c9407c882746fee1603e3a5d1d76a5576b7d9e5f0655ba8c91cd4cf7c3d"
API_URL = "https://app.daytona.io/api"
```

---


## SDK & Use Cases

Xem `references/sdk-and-usecases.md` cho: Python SDK usage, pre-installed packages, use cases chi tiết.

## Sandbox Lifecycle

```
Create → Use → Delete
  < 90ms    N phút    cleanup

Auto-stop: 15 phút idle
Auto-archive: 7 ngày
Auto-delete: manual only
```

**LUÔN LUÔN delete sau khi xong** — tránh tốn quota.

---

## Error Handling

```python
try:
    sandbox = daytona.create()
    resp = sandbox.process.exec("python3 script.py", timeout=60)
    if resp.exit_code != 0:
        print(f"Error: {resp.result}")
    else:
        print(f"Output: {resp.result}")
except Exception as e:
    print(f"Sandbox error: {e}")
finally:
    try:
        daytona.delete(sandbox)
    except:
        pass  # Best effort cleanup
```

---

## Cost Awareness

- Free tier: check app.daytona.io/dashboard
- Mỗi sandbox = 1 compute unit khi running
- **Tip:** Tạo → làm nhanh → xóa ngay. Đừng để idle.

---

## Security Note (quan trọng)

Sandbox là môi trường **isolated** — code chạy trong sandbox:
- Không access được VPS chính
- Không access được files workspace
- Network riêng (US IP)
→ An toàn để test untrusted code
→ **Không** paste API keys của anh vào untrusted code dù trong sandbox

## Mesh Connections
- **→ reader-adapter**: Scrape qua sandbox = IP sạch, không bị block
- **→ content-factory**: Chạy SEO pipeline song song trong sandbox
- **→ search-kit**: Research nặng cần isolated env

## Category
automation

## Trigger

Use this skill when:
- Cần chạy code trong sandbox an toàn
- Test script mà không ảnh hưởng hệ thống chính
- User says: "chạy code sandbox", "test script an toàn", "isolated run", "chạy trong sandbox"
