
"""Reconstruct agent sessions from normalized telemetry events."""

from collections import defaultdict
from datetime import datetime
from typing import Any


def _event_time(event: dict[str, Any]) -> datetime:
    """Parse a validated timezone-aware ISO 8601 timestamp."""
    value = event["timestamp"]
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(
            f"Event {event.get('event_id', '<unknown>')} "
            "has a timestamp without a timezone"
        )

    return parsed


def reconstruct_sessions(
    events: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Group events by session_id and order them deterministically.

    Events with the same timestamp are ordered by event_id.
    Duplicate events are preserved.
    The input list and event dictionaries are not modified.
    """
    sessions: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for event in events:
        session_id = event.get("session_id")
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("Every event must have a non-empty session_id")

        # Validate timestamp before adding an event to a session.
        _event_time(event)
        sessions[session_id].append(event)

    result: dict[str, list[dict[str, Any]]] = {}

    for session_id in sorted(sessions):
        result[session_id] = sorted(
            sessions[session_id],
            key=lambda event: (
                _event_time(event),
                str(event.get("event_id", "")),
            ),
        )

    return result
