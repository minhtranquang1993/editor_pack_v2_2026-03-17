---
name: hands-framework
description: Core framework cho Hands Pattern (lightweight stateful agent pattern). Use when skill khác cần import HandState, HandLogger, send_telegram, run_hand để chuẩn hóa flow quyết định và logging.
---

# HANDS Framework

Skill dạng thư viện, **không chạy trực tiếp**.

## Operational Notes

Import trong các Hand khác:

```python
import sys, os
sys.path.insert(0, os.path.join(WORKSPACE_DIR, "skills/hands-framework/scripts"))
from hands_core import HandState, HandLogger, send_telegram, run_hand
```

## Category
automation

## Trigger

Use this skill when:
- Skill khác cần import HandState hoặc HandLogger
- Cần shared state management giữa các skills
- User says: "dùng hands framework", "import HandState"

## Scripts

Library script — **không chạy trực tiếp**, import từ skill khác.

**File:** `scripts/hands_core.py`

Import pattern:
```python
import sys, os
sys.path.insert(0, os.path.join(WORKSPACE_DIR, "skills/hands-framework/scripts"))
from hands_core import HandState, HandLogger, send_telegram, run_hand
```

Exports:
- `HandState` — persistent state management (`state.json`)
- `HandLogger` — structured logging (`run.log`)
- `send_telegram(text, token_path, chat_id)` — Telegram alert với retry
- `run_hand(hand_name, steps, state, logger)` — step-based execution với resume logic
