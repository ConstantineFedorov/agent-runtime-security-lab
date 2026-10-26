
import json
import tempfile
import unittest
from pathlib import Path

from agent_runtime_security.ingest import read_jsonl, validate_event


def make_event(**overrides):
    event = {
        "event_id": "evt-001",
        "timestamp": "2026-10-19T10:00:00Z",
        "session_id": "sess-001",
        "source": "agentgateway",
        "event_type": "tool_call",
        "actor": "assistant",
        "data": {"tool_name": "search_docs"},
    }
    event.update(overrides)
    return event


class ValidateEventTests(unittest.TestCase):
    def test_accepts_valid_event(self):
        self.assertEqual(validate_event(make_event()), [])

    def test_rejects_non_object_event(self):
        self.assertIn(
            "Event must be a JSON object",
            validate_event(["not", "an", "object"]),
        )

    def test_rejects_missing_required_field(self):
        event = make_event()
        del event["session_id"]

        errors = validate_event(event)

        self.assertTrue(any("session_id" in error for error in errors))

    def test_rejects_invalid_timestamp(self):
        errors = validate_event(make_event(timestamp="not-a-date"))

        self.assertTrue(any("valid ISO 8601" in error for error in errors))

    def test_rejects_timestamp_without_timezone(self):
        errors = validate_event(
            make_event(timestamp="2026-10-19T10:00:00")
        )

        self.assertTrue(any("timezone" in error for error in errors))

    def test_rejects_non_object_data(self):
        errors = validate_event(make_event(data="not-an-object"))

        self.assertTrue(any("'data' must be a JSON object" in error for error in errors))


class ReadJsonlTests(unittest.TestCase):
    def read_text(self, content):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "events.jsonl"
            path.write_text(content, encoding="utf-8")
            return read_jsonl(path)

    def test_reads_valid_event(self):
        content = json.dumps(make_event()) + "\n"

        events, errors = self.read_text(content)

        self.assertEqual(len(events), 1)
        self.assertEqual(errors, [])
        self.assertEqual(events[0]["event_id"], "evt-001")

    def test_reports_malformed_json_and_continues(self):
        valid_line = json.dumps(make_event()) + "\n"
        content = valid_line + '{"event_id":\n' + json.dumps(
            make_event(event_id="evt-002")
        ) + "\n"

        events, errors = self.read_text(content)

        self.assertEqual(len(events), 2)
        self.assertEqual(len(errors), 1)
        self.assertIn("Line 2", errors[0])
        self.assertIn("invalid JSON", errors[0])

    def test_ignores_blank_lines(self):
        content = "\n  \n" + json.dumps(make_event()) + "\n"

        events, errors = self.read_text(content)

        self.assertEqual(len(events), 1)
        self.assertEqual(errors, [])

    def test_reports_invalid_event_and_keeps_valid_events(self):
        valid = json.dumps(make_event())
        invalid = json.dumps(make_event(timestamp="not-a-date"))
        content = valid + "\n" + invalid + "\n"

        events, errors = self.read_text(content)

        self.assertEqual(len(events), 1)
        self.assertEqual(len(errors), 1)
        self.assertIn("Line 2", errors[0])


if __name__ == "__main__":
    unittest.main()
