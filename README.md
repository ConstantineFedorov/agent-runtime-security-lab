# Agent Runtime Security Lab

> **AI Security · Runtime Monitoring · Agent Telemetry**

An educational prototype for collecting and correlating AI-agent runtime telemetry to identify suspicious semantic attack patterns across a session.

## Goal

Build a small, explainable AIDR-style prototype around an existing AI agent. The project objectives are:

1. Collect telemetry from at least one source (initially, a normalized JSONL event stream; an adapter for OpenCode or another agent gateway will be evaluated).
2. Correlate events and reconstruct an agent session.
3. Apply detection rules to the reconstructed sequence and produce evidence-backed findings.
4. Optionally add a second telemetry source after the first path is reliable.
5. Explore prevention/enforcement only after detection behavior is tested and clearly scoped.

The implementation is for learning and controlled testing, not a production security product.

## Planned architecture

```text
Agent / telemetry source
          |
          v
   Source adapter
          |
          v
  Normalized events (JSONL)
          |
          v
 Session correlation and reconstruction
          |
          v
 Explainable detection rules
          |
          v
 Findings + evidence + risk/severity
          |
          v
 JSON report / console summary
```

The initial implementation will use a documented internal event schema so that correlation and detection can be tested independently of a particular agent. A real source adapter will be added after checking the current source's event format and access model.

## Security principles

- Treat user content, retrieved content and tool results as untrusted data.
- Do not infer authorization from model-generated text.
- Preserve event timestamps, session identifiers and source provenance.
- Make findings explainable: each alert should reference the events and rules that triggered it.
- Fail visibly on malformed telemetry; do not silently manufacture missing fields.
- Keep secrets, real prompts, private logs and personal data out of committed fixtures.

## Repository status

**Status: project scaffold / implementation not yet started.**

No detection efficacy or test coverage is claimed yet. Findings and limitations will be documented as components are implemented and tested.

## Roadmap

- [ ] Define event schema and threat model.
- [ ] Add synthetic benign and attack-like fixtures.
- [ ] Implement JSONL ingestion and validation.
- [ ] Reconstruct sessions and correlate events by stable identifiers and event time.
- [ ] Add explainable semantic-attack detection rules.
- [ ] Add tests for positive, negative, malformed and out-of-order events.
- [ ] Evaluate a real telemetry source such as OpenCode or an agent gateway.
- [ ] Optionally integrate a second source.
- [ ] Assess safe prevention hooks and document limitations.

## Planned layout

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
├── .gitignore
└── README.md
```

This is a target layout; directories and implementation files will be added as we build the project.

## Development environment

The initial implementation targets Python 3.12+ and should use the standard library wherever it is sufficient. Exact runtime dependencies will be documented when needed.

## Reference

- [Actarea AIDR](https://github.com/actarea/aidr) — the example sensor referenced in the assignment. This repository is an independent educational project and does not claim endorsement by its authors.

## Responsible use

Use only agents and environments you own or are authorized to assess. Prefer synthetic fixtures for attack simulations. Do not commit API keys, tokens, private logs, or sensitive session content.
