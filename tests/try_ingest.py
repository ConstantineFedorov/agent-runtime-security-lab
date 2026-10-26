from agent_runtime_security.ingest import read_jsonl

events, errors = read_jsonl("tests/fixtures/sample.jsonl")

print(f"Valid events: {len(events)}")
print(f"Errors: {len(errors)}")

for event in events:
    print(event["event_id"], event["event_type"])

for error in errors:
    print("ERROR:", error)