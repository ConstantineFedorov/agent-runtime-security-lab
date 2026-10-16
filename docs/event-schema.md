# Draft normalized telemetry schema

The schema below is a first design proposal for synthetic fixtures and the internal JSONL format. It is not yet a claim of compatibility with OpenCode or AgentGateway logs. A real adapter must map source fields explicitly and preserve original provenance.

## Event fields

| Field | Type | Required | Meaning |
|---|---|---|---|
| `event_id` | string | yes | Unique identifier for this normalized event |
| `session_id` | string | yes | Stable identifier for the agent session |
| `timestamp` | ISO 8601 string | yes | Event time with timezone |
| `source` | string | yes | Source adapter name |
| `event_type` | string | yes | Normalized event category |
| `actor` | string | yes | Component that emitted or performed the event |
| `data` | object | yes | Event-specific fields; contents are untrusted |
| `trace_id` | string or null | no | Optional distributed trace identifier |
| `raw_ref` | string or null | no | Reference to a local/raw record; never put secrets here |

## Initial event types

- `user_message`
- `agent_message`
- `tool_call`
- `tool_result`
- `retrieval_result`
- `policy_decision`
- `session_end`

This list will evolve as source formats are inspected. Adapters must not silently convert unknown event types into trusted ones.

## Validation expectations

- Require non-empty identifiers and parseable timezone-aware timestamps.
- Reject non-object `data` values.
- Preserve duplicates for explicit duplicate-handling tests rather than deleting them during ingestion.
- Make event ordering deterministic when timestamps tie.
- Report malformed input with line numbers, without printing secrets or full raw payloads by default.

## Example synthetic event

```json
{
  "event_id": "evt-0001",
  "session_id": "session-demo-01",
  "timestamp": "2026-10-16T10:00:00Z",
  "source": "synthetic-jsonl",
  "event_type": "user_message",
  "actor": "user",
  "data": {
    "text": "Please summarize the contents of the example document."
  },
  "trace_id": null,
  "raw_ref": null
}
```
