#!/usr/bin/env python3
"""Capture candidate project context from VS Code agent hooks."""

from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path.cwd()
CONTEXT_DIR = ROOT / ".research" / "context" / "daily"

MAX_PROMPT_LENGTH = 8_000
MAX_RESPONSE_LENGTH = 2_000

MATERIAL_TOOL_NAMES = {
    "editFiles",
    "createFile",
    "runInTerminal",
    "runTests",
    "applyPatch",
}

SENSITIVE_MARKERS = {
    "password",
    "passwd",
    "api_key",
    "api-key",
    "secret",
    "access_token",
    "private_key",
}


def read_hook_input() -> dict[str, Any]:
    raw = sys.stdin.read()

    if not raw.strip():
        return {}

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid hook JSON: {exc}") from exc


def redact_text(text: str) -> str:
    """Avoid retaining obvious secret-bearing lines."""
    safe_lines = []

    for line in text.splitlines():
        lowered = line.lower()

        if any(marker in lowered for marker in SENSITIVE_MARKERS):
            safe_lines.append("[REDACTED: possible sensitive value]")
        else:
            safe_lines.append(line)

    return "\n".join(safe_lines)


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text

    return text[:limit] + "\n[TRUNCATED]"


def session_id(payload: dict[str, Any]) -> str:
    """Use a supplied session identifier when available."""
    for key in ("session_id", "sessionId", "conversation_id", "conversationId"):
        value = payload.get(key)
        if value:
            return str(value)

    seed = "|".join(
        [
            os.environ.get("VSCODE_PID", ""),
            str(ROOT.resolve()),
            datetime.now().strftime("%Y-%m-%d"),
        ]
    )

    return hashlib.sha256(seed.encode()).hexdigest()[:12]


def append_entry(entry: dict[str, Any]) -> None:
    CONTEXT_DIR.mkdir(parents=True, exist_ok=True)

    date = datetime.now().astimezone().date().isoformat()
    path = CONTEXT_DIR / f"{date}.jsonl"

    with path.open("a", encoding="utf-8") as handle:
        json.dump(entry, handle, ensure_ascii=False)
        handle.write("\n")


def capture_prompt(payload: dict[str, Any]) -> None:
    prompt = str(payload.get("prompt", "")).strip()

    if not prompt:
        return

    append_entry(
        {
            "timestamp": datetime.now().astimezone().isoformat(),
            "session_id": session_id(payload),
            "event": "user-prompt",
            "status": "unprocessed",
            "prompt": truncate(redact_text(prompt), MAX_PROMPT_LENGTH),
        }
    )


def capture_tool_result(payload: dict[str, Any]) -> None:
    tool_name = str(payload.get("tool_name", ""))

    if tool_name not in MATERIAL_TOOL_NAMES:
        return

    tool_input = payload.get("tool_input", {})
    tool_response = str(payload.get("tool_response", ""))

    append_entry(
        {
            "timestamp": datetime.now().astimezone().isoformat(),
            "session_id": session_id(payload),
            "event": "tool-result",
            "status": "unprocessed",
            "tool_name": tool_name,
            "tool_use_id": payload.get("tool_use_id"),
            "tool_input": tool_input,
            "tool_response": truncate(
                redact_text(tool_response),
                MAX_RESPONSE_LENGTH,
            ),
        }
    )


def capture_compaction(payload: dict[str, Any]) -> None:
    append_entry(
        {
            "timestamp": datetime.now().astimezone().isoformat(),
            "session_id": session_id(payload),
            "event": "pre-compact",
            "status": "unprocessed",
            "trigger": payload.get("trigger", "unknown"),
        }
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: capture_context.py "
            "{user-prompt|tool-result|pre-compact}"
        )

    event = sys.argv[1]
    payload = read_hook_input()

    handlers = {
        "user-prompt": capture_prompt,
        "tool-result": capture_tool_result,
        "pre-compact": capture_compaction,
    }

    try:
        handler = handlers[event]
    except KeyError as exc:
        raise SystemExit(f"Unsupported event: {event}") from exc

    handler(payload)

    # Hooks may return an empty JSON object when no agent control is required.
    print("{}")


if __name__ == "__main__":
    main()