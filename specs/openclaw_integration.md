# Project Chimera — OpenClaw agent network integration

**Document type:** Integration specification for agent social networks  
**Audience:** AI agents, platform engineers, OpenClaw / agent-network operators  
**Assumption:** Chimera participates as a first-class agent in an Agent Social Network (e.g. OpenClaw).

This document describes how Chimera **advertises itself**, **exposes capabilities and status**, and **handles security and trust** when integrating with OpenClaw or similar agent networks. It does not prescribe implementation details (protocol, transport, or library choices) unless needed for interoperability.

---

## 1. Purpose of integration

- **Discoverability:** Other agents and orchestrators can discover Chimera and understand what it can do.
- **Coordination:** Chimera can receive requests (e.g. collaboration, delegation) from the network and respond in a defined way.
- **Status and health:** The network can see whether Chimera is available and in what capacity.
- **Trust:** Integration is done in a way that respects security boundaries and does not weaken governance.

---

## 2. What Chimera publishes to the network

### 2.1 Availability

- Chimera (or each Chimera agent) **advertises that it is online and accepting work** within the network.
- **Availability** means: the agent process is running, not paused by governance, and not in a maintenance window (if applicable).
- Unavailability must be advertised or implied when the agent is paused, shutting down, or in a failure state that prevents it from fulfilling requests.

### 2.2 Capabilities

Chimera exposes **what** it can do, not implementation details. Recommended capability labels (or equivalent in the network’s schema) include:

| Capability | Description |
|------------|-------------|
| `content_planning` | Can produce content plans from trends and identity. |
| `content_generation` | Can generate text, image, and/or video content. |
| `content_publishing` | Can publish to configured platforms. |
| `trend_discovery` | Can consume and filter trend signals. |
| `evaluation` | Can evaluate content for quality and safety. |

- Capabilities may be scoped per **agent** (e.g. one Chimera agent only does planning, another does generation). The network schema may support capability sets per agent id.
- Chimera does **not** expose internal APIs or credentials; only high-level capability labels and required request/response shapes as defined in the technical spec.

### 2.3 Status

- **Status** includes at least: **available**, **busy**, **paused**, **unavailable**.
  - **available** — Ready to accept requests.
  - **busy** — Temporarily not accepting new work (e.g. rate limit or internal queue full).
  - **paused** — Governance or human action has paused the agent.
  - **unavailable** — Error or maintenance; no requests accepted.
- Status may be accompanied by an optional **message** or **reason** for debugging or operator visibility (e.g. "paused for approval backlog").
- **Timestamps:** Status updates should include a **last_updated** (or equivalent) so consumers can detect stale data.

---

## 3. Metadata exposed to the network

The following metadata should be exposable to the OpenClaw (or equivalent) network. Exact field names and format depend on the network’s API; the concepts below are the minimum.

| Metadata | Description | Example / notes |
|----------|-------------|------------------|
| `agent_id` | Unique identifier for this Chimera agent in the network. | Stable across restarts. |
| `display_name` | Human-readable name. | e.g. "Chimera-Influencer-1". |
| `capabilities` | List of capability labels. | As in section 2.2. |
| `status` | Current status. | As in section 2.3. |
| `status_message` | Optional reason or detail. | Free text. |
| `last_updated` | When status/capabilities were last updated. | ISO 8601. |
| `version` | Chimera or agent version for compatibility. | e.g. "0.1.0". |
| `platforms` | List of platforms this agent can publish to (optional). | e.g. ["youtube", "twitter"]. |

- **No PII, secrets, or internal IDs** that could compromise security or privacy should be exposed. Platform names or high-level labels are fine; credentials or user ids are not.

---

## 4. Update frequency

- **Status:** Update when status changes (available → busy → available, or paused, etc.). Optionally refresh periodically (e.g. every N seconds) so the network does not treat the agent as dead if event-driven updates are missed.
- **Capabilities:** Update when configuration or deployment changes (e.g. new platform, new content type). Capabilities change less often than status.
- **Metadata:** Other fields (e.g. display_name, version) update on deploy or config change.
- Exact **polling interval** or **heartbeat** should be defined in the network’s integration guide; Chimera should support at least one of: push updates, or periodic registration/heartbeat that the network can rely on.

---

## 5. Security and trust

### 5.1 Authentication and authorization

- Chimera **must not** expose internal APIs or data stores directly to the network. Only a dedicated **integration endpoint or adapter** should speak the network’s protocol.
- Outbound registration or heartbeat to OpenClaw (or similar) must use **authenticated** channels (e.g. API key, OAuth, or mTLS) as defined by the network. Credentials must be stored and used in a secure way (e.g. secrets manager, env, not in code).
- Inbound requests from the network (e.g. "create content for trend X") must be **authorized**: only accept calls that the network is allowed to make (e.g. by role or contract). Chimera should verify the caller’s identity and permissions before performing work.

### 5.2 Data and governance

- Chimera must **not** send content, PII, or internal metrics to the network unless required by a ratified integration contract. What is published is **availability, capabilities, status, and the metadata in section 3**.
- Any data received from the network (e.g. trend signals, collaboration requests) must be treated as **untrusted input**: validated and sanitized before use in planning or generation.
- Human oversight and escalation rules (see `_meta.md` and `functional.md`) **still apply** when Chimera acts on requests from the network. The network does not bypass governance.

### 5.3 Failure and isolation

- If the network is unreachable or misbehaves, Chimera should **degrade gracefully**: e.g. continue local operation, mark "network status unknown" or "unavailable" without crashing.
- Failures in the OpenClaw integration must **not** compromise the rest of Chimera (no single point of failure). Isolate integration in a component that can be disabled or restarted independently if needed.

---

## 6. Summary

- **Publish:** Availability, capabilities, status, and safe metadata to the OpenClaw (or equivalent) agent network.
- **Update:** Status on change (and optionally on a heartbeat); capabilities and metadata on config/deploy change.
- **Security:** Authenticate outbound and authorize inbound; no internal leakage; treat network input as untrusted; preserve governance.
- **Resilience:** Isolate integration so that network issues do not bring down Chimera.

Implementation of the actual protocol (e.g. MCP, custom REST, or OpenClaw-specific API) belongs in design and code; this spec defines the **what** and **constraints** for that implementation.
