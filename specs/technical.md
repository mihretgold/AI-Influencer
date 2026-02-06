# Project Chimera — Technical Specification

**Document type:** API contracts and data model  
**Audience:** AI agents, developers, integration partners  

This document defines **what** inputs and outputs agents and services use. It does not specify transport (REST, queue, etc.) unless required for correctness.

---

## A. API contracts

All payloads are JSON unless otherwise stated. Required fields must always be present; optional fields may be omitted. Error cases are described per action.

---

### A.1 fetch_trends

**Purpose:** Return trend signals for use in content planning.

**Input (request):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Identifier of the agent requesting trends. |
| `sources` | string[] | No | Filter to these source identifiers; if omitted, all configured sources. |
| `since` | string (ISO 8601) | No | Only return trends observed after this time. |
| `limit` | integer | No | Max number of trends to return; default and cap defined by implementation. |

**Output (success):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trends` | array | Yes | List of trend objects. |
| `trends[].id` | string | Yes | Unique trend identifier. |
| `trends[].source` | string | Yes | Source identifier (e.g. platform or feed name). |
| `trends[].type` | string | Yes | One of: `topic`, `hashtag`, `format`, `platform_signal`. |
| `trends[].label` | string | Yes | Human-readable label (e.g. topic or hashtag text). |
| `trends[].observed_at` | string (ISO 8601) | Yes | When this trend was observed. |
| `trends[].metadata` | object | No | Source-specific key-value metadata. |

**Error cases:**

- `400` — Invalid `agent_id`, invalid `since`, or `limit` out of range.
- `503` — Trend source unavailable; retry with backoff.

---

### A.2 generate_content

**Purpose:** Request generation of content (text and/or media) for a plan slot.

**Input (request):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_id` | string | Yes | Agent requesting generation. |
| `slot_id` | string | Yes | Content plan slot this generation fulfills. |
| `content_type` | string | Yes | One of: `text`, `image`, `video`, `text_and_image`, `text_and_video`. |
| `topic` | string | No | Topic or trend label to align with. |
| `platform` | string | Yes | Target platform (for format constraints). |
| `constraints` | object | No | See constraints sub-schema below. |
| `context_refs` | string[] | No | Optional memory or content IDs to use as context. |

**constraints (optional):**

| Field | Type | Description |
|-------|------|-------------|
| `max_text_length` | integer | Max characters for captions/titles. |
| `required_disclosures` | string[] | e.g. "AI-generated". |
| `prohibited_topics` | string[] | Topics to avoid. |
| `aspect_ratio` | string | For image/video (e.g. "16:9"). |

**Output (success):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_id` | string | Yes | Internal content draft identifier. |
| `slot_id` | string | Yes | Echo of request slot_id. |
| `body` | object | Yes | Type-specific payload. |
| `body.text` | string | If text requested | Caption, script, or title. |
| `body.media_uri` | string | If image/video | Reference to generated asset (URL or storage id). |
| `body.metadata` | object | No | Format, dimensions, duration, etc. |
| `evaluation_pending` | boolean | Yes | True if content must be evaluated before publish. |

**Error cases:**

- `400` — Invalid `agent_id`, `slot_id`, `content_type`, or `platform`.
- `422` — Generation failed (e.g. safety filter); details in error body.
- `503` — Generator unavailable; retry with backoff.

---

### A.3 evaluate_content

**Purpose:** Run quality and safety evaluation on a content draft.

**Input (request):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_id` | string | Yes | Content draft to evaluate. |
| `agent_id` | string | Yes | Owner of the content. |
| `checks` | string[] | No | Requested checks: e.g. `safety`, `quality`, `policy`. If omitted, run all configured checks. |

**Output (success):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_id` | string | Yes | Echo of request. |
| `passed` | boolean | Yes | True only if all requested checks passed. |
| `results` | array | Yes | Per-check results. |
| `results[].check` | string | Yes | Check identifier. |
| `results[].passed` | boolean | Yes | Whether this check passed. |
| `results[].score` | number | No | Numeric score if applicable. |
| `results[].reason` | string | No | Short reason (especially if failed). |
| `action` | string | Yes | One of: `approve`, `reject`, `escalate`. Recommended next action. |

**Error cases:**

- `400` — Invalid `content_id` or `agent_id`.
- `404` — Content draft not found.
- `503` — Evaluator unavailable; retry with backoff.

---

### A.4 publish_content

**Purpose:** Publish an approved content draft to a platform.

**Input (request):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content_id` | string | Yes | Approved content draft. |
| `agent_id` | string | Yes | Owner of the content. |
| `platform` | string | Yes | Target platform. |
| `scheduled_at` | string (ISO 8601) | No | When to publish; if omitted, publish as soon as possible. |
| `idempotency_key` | string | No | Client-provided key for deduplication; if omitted, server may generate. |

**Output (success):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `publish_id` | string | Yes | Internal publish record id. |
| `content_id` | string | Yes | Echo of request. |
| `platform` | string | Yes | Echo of request. |
| `status` | string | Yes | One of: `scheduled`, `published`, `failed`. |
| `external_id` | string | No | Platform’s id for the published item (when status is `published`). |
| `published_at` | string (ISO 8601) | No | Actual publish time (when status is `published`). |
| `message` | string | No | Human-readable status or error message. |

**Error cases:**

- `400` — Invalid `content_id`, `agent_id`, or `platform`.
- `404` — Content not found or not in publishable state.
- `409` — Duplicate request (e.g. same idempotency_key already used).
- `422` — Content not approved or platform validation failed.
- `429` — Platform rate limit; retry after backoff.
- `503` — Platform or publisher unavailable; retry with backoff.

---

## B. Database schema (conceptual ERD)

The following entities and relationships support the above contracts and agent state. Stored data must support correctness, audit, and future extensibility. Implementation may use relational, document, or hybrid stores; the logical model is below.

---

### B.1 Agent identity

- **agent**  
  - `agent_id` (PK), `name`, `identity_config` (e.g. style, voice), `created_at`, `updated_at`, `status` (active / paused / retired).  
  - One agent has many content drafts, many publish records, and many performance metrics.

---

### B.2 Content and planning

- **content_plan**  
  - `plan_id` (PK), `agent_id` (FK), `period_start`, `period_end`, `created_at`, `status`.  
  - One plan has many slots.

- **content_slot**  
  - `slot_id` (PK), `plan_id` (FK), `platform`, `content_type`, `topic`, `scheduled_at`, `state` (planned / generating / ready / approved / published / failed / cancelled).  
  - One slot may have one or more content drafts over time (e.g. after regeneration).

- **content_draft**  
  - `content_id` (PK), `slot_id` (FK), `agent_id` (FK), `body` (text + media refs + metadata), `created_at`, `evaluation_result`, `approval_status` (pending / approved / rejected / escalated).  
  - Links to publish records when published.

---

### B.3 Publishing and platform

- **publish_record**  
  - `publish_id` (PK), `content_id` (FK), `agent_id` (FK), `platform`, `idempotency_key` (unique), `status` (scheduled / published / failed / cancelled), `scheduled_at`, `published_at`, `external_id`, `error_message`, `created_at`, `updated_at`.  
  - One publish_record per logical publish attempt; retries may update the same record or create new with same idempotency_key depending on policy.

- **platform_config**  
  - `platform_id` (PK), `name`, `adapter_type`, `config` (credentials, rate limits, format rules), `created_at`, `updated_at`.  
  - Referenced by content_slot and publish_record via platform name or id.

---

### B.4 Trends and memory

- **trend_snapshot**  
  - `trend_id` (PK), `source`, `type`, `label`, `observed_at`, `metadata` (JSON), `created_at`.  
  - Used for trend discovery and optional historical analysis; retention policy applies.

- **memory_entry**  
  - `entry_id` (PK), `agent_id` (FK), `type` (e.g. past_content, performance, feedback), `payload` (JSON), `created_at`, `expires_at` (optional).  
  - Queried by agent for context; retention and privacy rules apply.

---

### B.5 Performance and audit

- **performance_metric**  
  - `metric_id` (PK), `agent_id` (FK), `publish_id` (FK), `platform`, `metric_type` (e.g. views, likes, shares), `value`, `observed_at`, `created_at`.  
  - Used for self-evaluation and reporting.

- **audit_log**  
  - `log_id` (PK), `agent_id` (FK), `event_type` (e.g. publish, escalation, approval, override), `entity_type`, `entity_id`, `payload` (JSON), `actor` (agent or human id), `created_at`.  
  - Immutable; supports governance and debugging.

---

### B.6 State transitions

- **content_slot.state** and **publish_record.status** drive lifecycle. Transitions must be defined in a separate state-machine spec (e.g. planned → generating → ready → approved → published). Timestamps (`created_at`, `updated_at`, `published_at`, `scheduled_at`) are required for correctness and analytics.

---

## C. Extensibility notes

- New platforms: add **platform_config** and adapter; reuse **content_draft** and **publish_record**.
- New content types: extend **content_draft.body** and **generate_content** contract with new `content_type` and body shape.
- New checks: extend **evaluate_content** `checks` and `results`; store in **content_draft.evaluation_result`.
- New trend sources: extend **trend_snapshot** and **fetch_trends** contract as needed; keep `type` and `source` for filtering.
