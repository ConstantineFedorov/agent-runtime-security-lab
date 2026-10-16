# Initial threat model

## Objective

Identify suspicious semantic attack patterns in an AI-agent session by correlating runtime events rather than evaluating isolated text alone.

## Assets

- Agent instructions and task context.
- Tool execution capability and tool arguments.
- Retrieved documents and tool results.
- Secrets and sensitive data accessible to the agent.
- Session telemetry, findings and audit evidence.

## Trust boundaries

- User-to-agent input.
- Retrieved document/tool result to agent context.
- Agent planning to tool execution.
- Telemetry source to parser/correlator.
- Detector output to a possible enforcement component.

## Threat scenarios to model

1. **Indirect prompt injection:** untrusted retrieved content tries to redirect the agent's task.
2. **Instruction override followed by a tool call:** a sequence suggests that untrusted content affected a sensitive action.
3. **Data-access attempt:** a tool call or output suggests access to a protected resource outside the expected task.
4. **Telemetry evasion or corruption:** duplicate, missing, malformed or reordered events weaken session reconstruction.
5. **False positives:** benign security analysis or quoted attack examples resemble malicious instructions.

## Defensive goals

- Correlate related events and retain evidence supporting each alert.
- Distinguish an observed signal from a confirmed incident.
- Test benign lookalikes as well as attack-like sequences.
- Validate telemetry before processing it.
- Keep detection separate from authorization and enforcement.

## Out of scope for the first iteration

- Proving that an agent is safe.
- Detecting every possible semantic attack.
- Automatically blocking real production agent operations.
- Collecting sensitive telemetry from environments without explicit authorization.

This is an initial threat model. We will update it when the first telemetry source and its actual event fields are selected.
