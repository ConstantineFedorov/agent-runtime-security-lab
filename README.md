# Agent Runtime Security

> **AI Security · Runtime Telemetry · Session Correlation · Explainable Detection**
>
> A prototype for processing AI-agent runtime events and correlating them into sessions, as a foundation for explainable detection of suspicious behavior.

![Domain](https://img.shields.io/badge/domain-AI%20Security-17365D)
![Scope](https://img.shields.io/badge/scope-Runtime%20Telemetry-0F6B78)
![Validation](https://img.shields.io/badge/tests-16%20passing-2E6D4F)
![Status](https://img.shields.io/badge/status-Detection%20Foundation-596579)

## 1. Overview

The project builds a small, explainable runtime-monitoring pipeline around normalized AI-agent telemetry. It is designed to make event ingestion and session reconstruction testable independently of a specific agent or gateway.

**Current implementation:** JSONL ingestion, event validation, session grouping, deterministic event ordering, and unit tests. Semantic attack detection and findings/report generation are planned follow-up stages.

## 2. Current Verification

The local unit-test run completed successfully:

| Metric | Result |
|---|---:|
| Unit tests passed | **16 / 16** |
| Failed tests | 0 |
| Test command | `python -m unittest discover -s tests -v` |
| Published branch | `runtime-security` |
| Latest implementation commit | `56bff75` |

These results validate the tested ingestion and session-reconstruction behavior. They do not demonstrate detection of real attacks or production readiness.

## 3. Architecture

```text
Agent / telemetry source
          |
          v
   JSONL event stream
          |
          v
   Parsing and validation
          |
          v
 Session reconstruction
          |
          v
 Explainable detection rules  (planned)
          |
          v
 Findings + evidence + risk  (planned)
          |
          v
 JSON report / console summary  (planned)
```

## 4. Implemented Components

- **JSONL ingestion:** reads events line by line and skips blank lines.
- **Event validation:** checks required fields, object-shaped `data`, and timezone-aware ISO 8601 timestamps.
- **Error handling:** records malformed JSON and invalid events with line-specific diagnostics while continuing to process other records.
- **Session reconstruction:** groups events by `session_id` and orders them deterministically by timestamp and `event_id`.
- **Regression tests:** covers valid and invalid records, malformed JSON, blank lines, grouping, ordering, duplicate preservation, and missing timezone/session identifiers.

## 5. Security Principles

- Treat user content, retrieved content, and tool results as untrusted data.
- Do not infer authorization from model-generated text.
- Preserve event timestamps, session identifiers, and source provenance.
- Make future findings explainable by linking each alert to the events and rules that triggered it.
- Fail visibly on malformed telemetry; do not silently manufacture missing fields.
- Keep secrets, real prompts, private logs, and personal data out of committed fixtures.
- Keep detection separate from enforcement until detection behavior is tested and clearly scoped.

## 6. Repository Structure

```text
agent-runtime-security-lab/
├── docs/
│   ├── architecture.md
│   ├── event-schema.md
│   └── threat-model.md
├── src/
│   └── agent_runtime_security/
├── tests/
│   └── fixtures/
└── README.md
```

## 7. Roadmap

- [x] Define the initial event schema and threat model.
- [x] Implement JSONL ingestion and validation.
- [x] Reconstruct sessions with deterministic ordering.
- [x] Add unit tests for core ingestion and reconstruction behavior.
- [ ] Add synthetic benign and attack-like fixtures.
- [ ] Implement explainable semantic-attack detection rules.
- [ ] Produce findings with linked evidence and risk/severity rationale.
- [ ] Add end-to-end regression tests for ingest → session → detection → report.
- [ ] Evaluate a real telemetry source such as OpenCode or an agent gateway.
- [ ] Consider prevention hooks only after detection quality and limitations are documented.

## 8. Development and Testing

The implementation uses Python and the standard library for the current test suite. Run from the repository root:

```powershell
python -m unittest discover -s tests -v
```

## 9. Limitations

The current implementation prepares and orders telemetry; it does not yet implement semantic attack detection, risk scoring, or report generation. Synthetic tests verify defined cases and do not establish coverage of real-world agent behavior. Performance, fuzzing, and end-to-end integration have not yet been evaluated.

## 10. Related Work

- [DocsAgent Security Assessment](https://github.com/ConstantineFedorov/docsagent-security-assessment) — prompt injection across user input, RAG, and MCP metadata.
- [ADLC Agent Security Assessment](https://github.com/ConstantineFedorov/adlc-agent-security-assessment) — tool-result poisoning and runtime enforcement.
- [ADLC Server-Side Guardrails](https://github.com/ConstantineFedorov/adlc-server-side-guardrails) — policy and content enforcement controls.

## 11. Responsible Use

Use only agents and environments you own or are authorized to assess. Prefer synthetic fixtures for attack simulations. Do not commit API keys, tokens, private logs, or sensitive session content.
