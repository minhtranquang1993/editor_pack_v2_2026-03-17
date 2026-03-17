#!/usr/bin/env python3
"""
Hands Framework — Core library cho stateful agent pattern.

Cung cấp:
- HandState: persistent state management (state.json)
- HandLogger: structured logging (run.log)
- send_telegram(): Telegram alert với retry
- run_hand(): step-based execution với resume logic
"""

import json
import os
import tempfile
import time
from datetime import datetime, timedelta, timezone

# ---------------------------------------------------------------------------
# Timezone
# ---------------------------------------------------------------------------
ICT = timezone(timedelta(hours=7))


def _now_ict() -> datetime:
    return datetime.now(ICT)


def _now_iso() -> str:
    return _now_ict().strftime("%Y-%m-%dT%H:%M:%S+07:00")


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
def _workspace_dir() -> str:
    """Tìm workspace root (chứa folder skills/)."""
    d = os.path.dirname(os.path.abspath(__file__))
    # Đi lên tối đa 5 cấp để tìm folder có "skills/"
    for _ in range(5):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "skills")):
            return d
    # Fallback
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


WORKSPACE_DIR = _workspace_dir()


def _state_dir(hand_name: str) -> str:
    return os.path.join(WORKSPACE_DIR, "memory", "hands", hand_name)


def _state_path(hand_name: str) -> str:
    return os.path.join(_state_dir(hand_name), "state.json")


def _log_path(hand_name: str) -> str:
    return os.path.join(_state_dir(hand_name), "run.log")


# ---------------------------------------------------------------------------
# HandState
# ---------------------------------------------------------------------------
class HandState:
    """
    Quản lý persistent state cho 1 Hand.
    Lưu vào: memory/hands/{hand_name}/state.json
    """

    def __init__(self, hand_name: str, raw: dict):
        self.hand_name = hand_name
        self.status = raw.get("status", "idle")
        self.current_step = raw.get("current_step")
        self.last_run_at = raw.get("last_run_at")
        self.last_success_at = raw.get("last_success_at")
        self.run_count = raw.get("run_count", 0)
        self.consecutive_errors = raw.get("consecutive_errors", 0)
        self.last_error = raw.get("last_error")
        self.data = raw.get("data", {})
        self.updated_at = raw.get("updated_at", _now_iso())

    @staticmethod
    def load(hand_name: str) -> "HandState":
        """Đọc state.json, tạo mới nếu chưa có."""
        path = _state_path(hand_name)
        if os.path.exists(path):
            with open(path) as f:
                raw = json.load(f)
        else:
            raw = {"hand_name": hand_name}
        return HandState(hand_name, raw)

    def save(self) -> None:
        """Ghi state.json (atomic write: ghi temp file rồi rename)."""
        self.updated_at = _now_iso()
        d = _state_dir(self.hand_name)
        os.makedirs(d, exist_ok=True)
        path = _state_path(self.hand_name)
        data = {
            "hand_name": self.hand_name,
            "status": self.status,
            "current_step": self.current_step,
            "last_run_at": self.last_run_at,
            "last_success_at": self.last_success_at,
            "run_count": self.run_count,
            "consecutive_errors": self.consecutive_errors,
            "last_error": self.last_error,
            "data": self.data,
            "updated_at": self.updated_at,
        }
        # Atomic write: ghi temp rồi rename
        fd, tmp_path = tempfile.mkstemp(dir=d, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp_path, path)
        except Exception:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    def set_running(self, step: str) -> None:
        self.status = "running"
        self.current_step = step
        self.last_run_at = _now_iso()
        self.run_count += 1
        self.save()

    def set_done(self) -> None:
        self.status = "idle"
        self.current_step = None
        self.consecutive_errors = 0
        self.last_success_at = _now_iso()
        self.save()

    def set_error(self, msg: str) -> None:
        self.status = "error"
        self.last_error = msg
        self.consecutive_errors += 1
        self.save()

    def set_paused(self, step: str) -> None:
        self.status = "paused"
        self.current_step = step
        self.save()

    def get_data(self, key: str, default=None):
        return self.data.get(key, default)

    def set_data(self, key: str, value) -> None:
        self.data[key] = value
        self.save()


# ---------------------------------------------------------------------------
# HandLogger
# ---------------------------------------------------------------------------
class HandLogger:
    """
    Logger cho Hand. Ghi vào: memory/hands/{hand_name}/run.log
    Format: [YYYY-MM-DD HH:MM UTC] [LEVEL] message
    """

    def __init__(self, hand_name: str):
        self.hand_name = hand_name
        self._path = _log_path(hand_name)
        os.makedirs(os.path.dirname(self._path), exist_ok=True)

    def _write(self, level: str, msg: str):
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        with open(self._path, "a") as f:
            f.write(f"[{ts}] [{level}] {msg}\n")

    def info(self, msg: str):
        self._write("INFO", msg)

    def error(self, msg: str):
        self._write("ERROR", msg)

    def warn(self, msg: str):
        self._write("WARN", msg)


# ---------------------------------------------------------------------------
# Telegram
# ---------------------------------------------------------------------------
DEFAULT_CHAT_ID = "1661694132"


def send_telegram(text: str, token_path: str = "credentials/telegram_token.txt",
                  chat_id: str = DEFAULT_CHAT_ID) -> bool:
    """Gửi message Telegram, retry 1 lần sau 5s nếu fail."""
    import requests

    # Đọc token
    if not os.path.isabs(token_path):
        token_path = os.path.join(WORKSPACE_DIR, token_path)
    if not os.path.exists(token_path):
        return False
    with open(token_path) as f:
        token = f.read().strip()

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}

    for attempt in range(2):
        try:
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                return True
        except Exception:
            pass
        if attempt == 0:
            time.sleep(5)

    return False


# ---------------------------------------------------------------------------
# run_hand — Step-based execution với resume logic
# ---------------------------------------------------------------------------
def run_hand(hand_name: str, steps: list, state: HandState, logger: HandLogger):
    """
    Chạy Hand theo danh sách steps, có resume logic.

    steps = [
        {"name": "step_name", "fn": callable, "skip_if_done": bool},
        ...
    ]

    - Nếu state.status == "paused" và current_step = "X" → skip các step trước X, resume từ X
    - Mỗi step: gọi fn(), nếu exception → set_error + log + raise
    - Xong hết → set_done()
    """
    # Determine resume point
    resume_from = None
    if state.status == "paused" and state.current_step:
        resume_from = state.current_step
        logger.info(f"Resuming from step: {resume_from}")

    found_resume_point = resume_from is None  # Nếu không resume thì bắt đầu từ đầu

    for step in steps:
        step_name = step["name"]
        fn = step["fn"]
        skip_if_done = step.get("skip_if_done", False)

        # Skip logic khi resume
        if not found_resume_point:
            if step_name == resume_from:
                found_resume_point = True
            else:
                logger.info(f"Skipping step (resume): {step_name}")
                continue

        # Execute step
        state.set_running(step_name)
        logger.info(f"Running step: {step_name}")
        try:
            fn()
            logger.info(f"Step done: {step_name}")
        except Exception as e:
            state.set_error(str(e))
            logger.error(f"Step failed: {step_name} — {e}")
            raise

    # Safety check: nếu resume nhưng không tìm thấy step → error
    if not found_resume_point:
        err_msg = f"Resume step '{resume_from}' not found in steps list"
        state.set_error(err_msg)
        logger.error(err_msg)
        raise RuntimeError(err_msg)

    state.set_done()
    logger.info(f"Hand '{hand_name}' completed all steps")
