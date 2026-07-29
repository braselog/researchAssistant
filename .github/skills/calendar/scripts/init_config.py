#!/usr/bin/env python3
"""
Initialize calendar configuration for DEFAULT_CALENDARS and DEFAULT_WRITE_CALENDAR.

This script:
1. Checks .env for calendar defaults
2. If missing, lists available calendars
3. Prompts user to select defaults
4. Updates .env with selected values
"""

import os
import re
import sys
import subprocess
from pathlib import Path
from typing import List

try:
    from dotenv import load_dotenv, set_key
except ImportError:
    print("❌ Error: Required package not installed")
    print("  conda run -n research-assistant pip install python-dotenv")
    sys.exit(1)


ANSI_RE = re.compile(r"\x1B\[[0-9;]*[mK]")


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def get_cli_path() -> Path:
    return Path(__file__).resolve().parent / "calendar-cli.sh"


def load_env(env_file: Path) -> None:
    if env_file.exists():
        load_dotenv(env_file)
    else:
        print(f"❌ Error: .env file not found at {env_file}")
        print("  Create it first: cp .env.example .env")
        sys.exit(1)


def list_available_calendars(wrapper_path: Path) -> List[str]:
    cmd = ["bash", str(wrapper_path), "calendars"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    output = (result.stdout or "") + "\n" + (result.stderr or "")
    output = strip_ansi(output)

    if result.returncode != 0:
        print("❌ Error listing calendars. Ensure Calendar access and icalBuddy are configured.")
        print(output.strip())
        sys.exit(1)

    calendars: List[str] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "Available Calendars" in line:
            continue
        if line.startswith(("ℹ", "✓", "⚠", "Error:", "Warning")):
            continue
        if all(ch in "━-" for ch in line):
            continue

        # Only process lines that start with bullet points (calendar names)
        if line.startswith("•"):
            cleaned = re.sub(r"^[\-\*•]\s*", "", line).strip()
            if cleaned and cleaned not in calendars:
                calendars.append(cleaned)

    if not calendars:
        print("❌ No calendars found in output. Open Calendar.app and ensure calendars are visible.")
        sys.exit(1)

    # Sort calendars alphabetically for easier selection
    calendars.sort()
    return calendars


def prompt_multi_select(calendars: List[str]) -> List[str]:
    print("\n📋 Select calendars to include by default:")
    for idx, cal in enumerate(calendars, start=1):
        print(f"  [{idx}] {cal}")

    while True:
        choice = input(f"\nEnter comma-separated numbers [1-{len(calendars)}] or 'all': ").strip().lower()
        if choice == "all":
            return calendars

        parts = [p.strip() for p in choice.split(",") if p.strip()]
        if not parts:
            print("⚠️  Please enter at least one selection.")
            continue

        try:
            indexes = [int(p) for p in parts]
        except ValueError:
            print("⚠️  Please enter valid numbers separated by commas.")
            continue

        if any(i < 1 or i > len(calendars) for i in indexes):
            print(f"⚠️  Selections must be between 1 and {len(calendars)}.")
            continue

        selected = [calendars[i - 1] for i in indexes]
        return selected


def prompt_single_select(calendars: List[str], default_value: str) -> str:
    print("\n📌 Select the calendar to write new events to:")
    for idx, cal in enumerate(calendars, start=1):
        print(f"  [{idx}] {cal}")

    default_index = calendars.index(default_value) + 1 if default_value in calendars else 1
    while True:
        choice = input(f"\nEnter choice [1-{len(calendars)}] (default {default_index}): ").strip()
        if not choice:
            return calendars[default_index - 1]
        try:
            index = int(choice)
        except ValueError:
            print("⚠️  Please enter a valid number.")
            continue
        if 1 <= index <= len(calendars):
            return calendars[index - 1]
        print(f"⚠️  Selection must be between 1 and {len(calendars)}.")


def main() -> None:
    project_root = get_project_root()
    env_file = project_root / ".env"
    cli_path = get_cli_path()

    load_env(env_file)

    default_calendars = os.getenv("DEFAULT_CALENDARS", "").strip()
    default_write_calendar = os.getenv("DEFAULT_WRITE_CALENDAR", "").strip()

    if default_calendars and default_write_calendar:
        print("✓ Calendar defaults already configured in .env")
        print(f"  DEFAULT_CALENDARS={default_calendars}")
        print(f"  DEFAULT_WRITE_CALENDAR={default_write_calendar}")
        return

    calendars = list_available_calendars(cli_path)

    if not default_calendars:
        selected = prompt_multi_select(calendars)
        set_key(str(env_file), "DEFAULT_CALENDARS", ",".join(selected))
        print(f"✓ Updated DEFAULT_CALENDARS in .env")
    else:
        selected = [c.strip() for c in default_calendars.split(",") if c.strip()]

    if not default_write_calendar:
        write_calendar = prompt_single_select(calendars, selected[0])
        set_key(str(env_file), "DEFAULT_WRITE_CALENDAR", write_calendar)
        print("✓ Updated DEFAULT_WRITE_CALENDAR in .env")

    print("\n✅ Calendar defaults configured.")


if __name__ == "__main__":
    main()
