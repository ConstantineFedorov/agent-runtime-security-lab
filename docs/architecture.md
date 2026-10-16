# Architecture (initial design)

## Processing stages

1. **Ingestion** — read records from a telemetry adapter or JSONL file.
2. **Validation and normalization** — reject malformed records and map valid events to the internal schema while preserving source provenance.
3. **Session reconstruction** — group events by a stable session identifier and order them using event time, with explicit handling for missing or conflicting timestamps.
4. **Detection** — evaluate transparent rules over event sequences; a detection is a hypothesis supported by evidence, not proof of compromise.
5. **Reporting** — emit structured findings with rule identifier, severity, event references and rationale.

## Trust boundaries

- Agent and model output are not trusted authorization decisions.
- Tool results and retrieved content may contain prompt-injection attempts.
- Telemetry itself may be incomplete, duplicated, delayed, malformed or adversarially crafted.
- The detector must not execute tools or change an agent's permissions.
- Prevention, if added, must be a separate, explicit enforcement boundary with tests for fail-open and fail-closed behavior.

## Design constraints

- Keep ingestion, correlation and detection independently testable.
- Prefer deterministic, explainable rules for the first version.
- Do not label a session malicious based only on a keyword.
- Include counterexamples and benign fixtures to measure false positives.
- Keep synthetic test fixtures free of live secrets and sensitive data.

This document describes the intended design. It does not claim these components have been implemented yet.
