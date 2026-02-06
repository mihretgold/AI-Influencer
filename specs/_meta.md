# Project Chimera — Master Meta Specification

**Document type:** Constitution / source of truth for the system  
**Audience:** AI agents, developers, governance  
**Version:** 0.1.0

---

## 1. High-level vision

**Project Chimera** is a long-lived **autonomous influencer system**. It operates as a network of AI influencer agents that:

- **Perceive** external trends, platform signals, and audience feedback.
- **Plan** content calendars and creative direction aligned with agent identity and goals.
- **Generate** text, image, and video content within explicit safety and brand constraints.
- **Publish** to multiple platforms on a schedule, with correct platform-specific formatting and metadata.
- **Evaluate** their own performance and content quality, and correct or escalate when thresholds are not met.
- **Evolve** over time within governance boundaries and with human oversight.

Chimera is built for **durability**: agents run continuously, persist memory and state, and integrate with external agent networks (e.g. OpenClaw) as first-class participants. The system is **platform-independent** in design: support for new platforms is added via configuration and adapters, not by changing core agent logic.

---

## 2. Non-goals (what Chimera is not)

The following are **explicitly out of scope** unless later specified in a ratified spec change:

- **Chimera is not a general-purpose chatbot or assistant.** It is specialized for influencer-style content creation, publishing, and trend response.
- **Chimera is not a replacement for human creators.** It operates under human-defined identity, guardrails, and approval workflows where required.
- **Chimera does not hold or manage user payment instruments.** Monetization and payouts are handled by platforms or external systems; Chimera may consume read-only monetization metrics.
- **Chimera is not a single monolithic app.** It is a system of agents, services, and data stores; "Chimera" refers to the system and its agents collectively.
- **Chimera does not guarantee real-time latency.** Scheduling, batching, and retries are first-class; sub-second response times are not a primary success criterion for content pipelines.
- **Chimera does not interpret unwritten or implicit intent.** All business intent must be expressed in written specifications, config, or explicit human inputs.

---

## 3. Core constraints

### 3.1 Safety and compliance

- **Content must not violate platform ToS or applicable law.** Agents must use explicit content policies and safety checks before publishing.
- **No deceptive identity.** Agent identity (e.g. "AI-generated") must be disclosed where required by platform or regulation.
- **No generation of harmful or prohibited content.** Safety filters and human escalation paths are mandatory for sensitive or high-reach content.
- **Audit trail.** All publish decisions, escalations, and key state transitions must be logged for review and compliance.

### 3.2 Governance and human oversight

- **Human-in-the-loop where specified.** Approval gates, escalation rules, and override capabilities must be configurable and enforced.
- **Identity and voice are human-defined.** Agents do not invent long-term persona or brand; they operate within declared identity and style guides.
- **Governance rules are versioned and traceable.** Changes to safety, approval, or escalation rules are recorded and attributable.

### 3.3 Scale and operability

- **Designed for multiple agents and platforms.** Schema, APIs, and workflows must support N agents and M platforms without redesign.
- **Idempotency and retries.** Publish and external API calls must be designed for safe retries and duplicate detection.
- **Graceful degradation.** Failures in one platform or one agent must not bring down the whole system; isolation and circuit-breaking are required.

### 3.4 Platform independence

- **No hard-coded platform assumptions in core logic.** Platform-specific behavior lives in adapters, config, and schemas.
- **Unified internal representation.** Content and metadata are stored in a platform-agnostic form; translation to platform formats happens at publish time.

---

## 4. Success criteria

The system is considered successful when:

1. **Agents can run unattended** for defined cycles: trend discovery → plan → generate → evaluate → publish, with no manual steps unless escalation or approval is triggered.
2. **Content meets quality and safety bars** as defined in specs and config; violations are caught by evaluation or safety checks and escalated or blocked.
3. **Publishing is correct and traceable:** the right content reaches the right platform with correct metadata, and every publish is logged with agent, content id, platform, and timestamp.
4. **Human oversight works:** approval queues, escalation reasons, and override actions are visible and actionable; auditors can reconstruct decisions from logs.
5. **Specifications remain the source of truth:** agents and developers treat `specs/` (and ratified extensions) as authoritative; behavior that contradicts the specs is a defect.
6. **Integration with agent networks is possible:** Chimera can advertise itself, its capabilities, and status to networks such as OpenClaw in a defined, secure way.

---

## 5. Document authority

- **This document** (`_meta.md`) defines vision, non-goals, constraints, and success criteria. Changes require explicit ratification.
- **Functional and technical specs** in this directory elaborate *what* the system must do and *what* contracts and data it uses; they do not prescribe implementation.
- **AI agents cannot read intent unless it is explicitly written.** When in doubt, add a clear, written constraint or user story rather than relying on implicit understanding.
