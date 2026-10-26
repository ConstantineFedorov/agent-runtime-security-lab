
"""Read and validate JSONL telemetry events."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED_STRING_FIELDS = (
    "event_id",
    "timestamp",
    "session_id",
    "source",
    "event_type",
    "actor",
)


def validate_event(event: Any) -> list[str]:
    """Return validation errors for one decoded JSON event."""
    errors: list[str] = []

    if not isinstance(event, dict):
        return ["Event must be a JSON object"]

    for field in REQUIRED_STRING_FIELDS:
        value = event.get(field)

        if not isinstance(value, str) or not value.strip():
            errors.append(
                f"Field '{field}' must be a non-empty string"
            )

    timestamp = event.get("timestamp")
    if isinstance(timestamp, str) and timestamp.strip():
        try:
            parsed_timestamp = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
            if parsed_timestamp.tzinfo is None:
                errors.append(
                    "Field 'timestamp' must include a timezone"
                )
            elif parsed_timestamp.utcoffset() is None:
                errors.append(
                    "Field 'timestamp' must include a valid timezone"
                )
        except ValueError:
            errors.append(
                "Field 'timestamp' must be a valid ISO 8601 datetime"
            )

    if "data" not in event:
        errors.append("Missing required field 'data'")
    elif not isinstance(event["data"], dict):
        errors.append("Field 'data' must be a JSON object")

    return errors


def read_jsonl(path: str | Path) -> tuple[list[dict[str, Any]], list[str]]:
    """Read JSONL, returning valid events and line-specific errors."""
    events: list[dict[str, Any]] = []
    errors: list[str] = []

    file_path = Path(path)

    try:
        with file_path.open("r", encoding="utf-8-sig") as file:
            for line_number, raw_line in enumerate(file, start=1):
                if not raw_line.strip():
                    continue

                try:
                    event = json.loads(raw_line)
                except json.JSONDecodeError as exc:
                    errors.append(
                        f"Line {line_number}: invalid JSON "
                        f"(column {exc.colno}: {exc.msg})"
                    )
                    continue

                event_errors = validate_event(event)

                if event_errors:
                    for error in event_errors:
                        errors.append(
                            f"Line {line_number}: {error}"
                        )
                    continue

                events.append(event)

    except OSError as exc:
        errors.append(
            f"Cannot read file '{file_path}': {exc}"
        )

    return events, errors
