# Skill: Publish Content

**Spec reference:** `specs/technical.md` § A.4 (publish_content)  
**Type:** Runtime agent skill — no implementation in this repo; contract only.

---

## Purpose

Publish an **approved** content draft to a platform. The skill defines the input/output contract for publishing; it does not implement the platform adapter. Content MUST be in an approved state before publish; otherwise the skill returns an error. Idempotency is supported via `idempotency_key`.

---

## Inputs (JSON schema)

Request body MUST be valid JSON with the following shape.

```json
{
  "content_id": "<string, required>",
  "agent_id": "<string, required>",
  "platform": "<string, required>",
  "scheduled_at": "<string, ISO 8601, optional>",
  "idempotency_key": "<string, optional>"
}
```

| Field             | Type   | Required | Description |
|-------------------|--------|----------|-------------|
| `content_id`      | string | Yes      | Approved content draft to publish. |
| `agent_id`        | string | Yes      | Owner of the content. |
| `platform`        | string | Yes      | Target platform. |
| `scheduled_at`    | string | No       | When to publish; if omitted, publish as soon as possible (ISO 8601). |
| `idempotency_key` | string | No       | Client-provided key for deduplication; if omitted, server may generate. |

---

## Outputs (JSON schema)

Success response:

```json
{
  "publish_id": "<string, required>",
  "content_id": "<string, required>",
  "platform": "<string, required>",
  "status": "scheduled | published | failed",
  "external_id": "<string, optional>",
  "published_at": "<string, ISO 8601, optional>",
  "message": "<string, optional>"
}
```

| Field          | Type   | Required | Description |
|----------------|--------|----------|-------------|
| `publish_id`   | string | Yes      | Internal publish record id. |
| `content_id`   | string | Yes      | Echo of request. |
| `platform`     | string | Yes      | Echo of request. |
| `status`       | string | Yes      | One of: `scheduled`, `published`, `failed`. |
| `external_id`  | string | No       | Platform’s id for the published item (when status is `published`). |
| `published_at` | string | No       | Actual publish time (when status is `published`). |
| `message`      | string | No       | Human-readable status or error message. |

---

## Error conditions

| Code | Condition | Client action |
|------|------------|----------------|
| `400` | Invalid `content_id`, `agent_id`, or `platform`. | Fix request and retry. |
| `404` | Content not found or not in publishable (approved) state. | Ensure content exists and is approved; do not retry same request. |
| `409` | Duplicate request (e.g. same `idempotency_key` already used). | Treat as already handled; do not retry with same key. |
| `422` | Content not approved or platform validation failed. | Resolve approval or validation; then retry. |
| `429` | Platform rate limit. | Retry after backoff (e.g. Retry-After header). |
| `503` | Platform or publisher unavailable. | Retry with backoff. |

Error response body SHOULD include a machine-readable code and an optional human-readable `message`.

---

## Example usage

**Request (publish now):**

```json
{
  "content_id": "draft-video-abc123",
  "agent_id": "chimera-influencer-1",
  "platform": "youtube",
  "idempotency_key": "publish-slot-xyz-001-20250206"
}
```

**Response (success, published):**

```json
{
  "publish_id": "pub-001",
  "content_id": "draft-video-abc123",
  "platform": "youtube",
  "status": "published",
  "external_id": "yt-video-id-xyz",
  "published_at": "2025-02-06T14:00:00Z",
  "message": "Published successfully."
}
```

**Response (success, scheduled):**

```json
{
  "publish_id": "pub-002",
  "content_id": "draft-video-def456",
  "platform": "twitter",
  "status": "scheduled",
  "message": "Scheduled for 2025-02-07T09:00:00Z."
}
```

**Response (error 422):**

```json
{
  "code": "422",
  "message": "Content not approved or platform validation failed."
}
```

**Response (error 429):**

```json
{
  "code": "429",
  "message": "Platform rate limit; retry after backoff.",
  "retry_after_seconds": 60
}
```
