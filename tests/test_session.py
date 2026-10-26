
import unittest

from agent_runtime_security.session import reconstruct_sessions


def make_event(event_id, session_id, timestamp):
    return {
        "event_id": event_id,
        "session_id": session_id,
        "timestamp": timestamp,
        "source": "synthetic-jsonl",
        "event_type": "tool_call",
        "actor": "assistant",
        "data": {},
    }


class ReconstructSessionsTests(unittest.TestCase):
    def test_groups_events_by_session(self):
        events = [
            make_event("evt-1", "sess-A", "2026-10-19T10:00:00Z"),
            make_event("evt-2", "sess-B", "2026-10-19T10:00:01Z"),
            make_event("evt-3", "sess-A", "2026-10-19T10:00:02Z"),
        ]

        sessions = reconstruct_sessions(events)

        self.assertEqual(set(sessions), {"sess-A", "sess-B"})
        self.assertEqual(
            [e["event_id"] for e in sessions["sess-A"]],
            ["evt-1", "evt-3"],
        )

    def test_orders_events_by_timestamp(self):
        events = [
            make_event("evt-2", "sess-A", "2026-10-19T10:00:02Z"),
            make_event("evt-1", "sess-A", "2026-10-19T10:00:01Z"),
        ]

        sessions = reconstruct_sessions(events)

        self.assertEqual(
            [e["event_id"] for e in sessions["sess-A"]],
            ["evt-1", "evt-2"],
        )

    def test_ties_are_ordered_by_event_id(self):
        events = [
            make_event("evt-b", "sess-A", "2026-10-19T10:00:00Z"),
            make_event("evt-a", "sess-A", "2026-10-19T10:00:00Z"),
        ]

        sessions = reconstruct_sessions(events)

        self.assertEqual(
            [e["event_id"] for e in sessions["sess-A"]],
            ["evt-a", "evt-b"],
        )

    def test_preserves_duplicate_events(self):
        event = make_event("evt-1", "sess-A", "2026-10-19T10:00:00Z")

        sessions = reconstruct_sessions([event, event.copy()])

        self.assertEqual(len(sessions["sess-A"]), 2)

    def test_rejects_missing_session_id(self):
        event = make_event("evt-1", "sess-A", "2026-10-19T10:00:00Z")
        event["session_id"] = ""

        with self.assertRaises(ValueError):
            reconstruct_sessions([event])

    def test_rejects_timestamp_without_timezone(self):
        event = make_event("evt-1", "sess-A", "2026-10-19T10:00:00")

        with self.assertRaises(ValueError):
            reconstruct_sessions([event])


if __name__ == "__main__":
    unittest.main()
