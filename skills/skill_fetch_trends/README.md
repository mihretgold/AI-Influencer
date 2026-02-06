# Skill: Fetch Trends

**Spec reference:** `specs/technical.md` § A.1 (fetch_trends)  
**Type:** Runtime agent skill — no implementation in this repo; contract only.

---

## Purpose

Return trend signals from configured sources so that the agent can use them for content planning and timing. The skill normalizes and filters trends; it does not define where trends are stored or how they are ingested.

---

## Inputs (JSON schema)

Request body MUST be valid JSON with the following shape.

```json
{
  "agent_id": "<string, required>",
  "sources": ["<string>"],
  "since": "<string, ISO 8601 datetime, optional>",
  "limit": "<integer, optional>"
}
```

| Field      | Type    | Required | Description |
|------------|---------|----------|-------------|
| `agent_id` | string  | Yes      | Identifier of the agent requesting trends. |
| `sources`  | string[]| No       | Filter to these source identifiers; if omitted, all configured sources. |
| `since`    | string  | No       | Only return trends observed after this time (ISO 8601). |
| `limit`    | integer | No       | Maximum number of trends to return; default and cap defined by implementation. |

---

## Outputs (JSON schema)

Success response:

```json
{
  "trends": [
    {
      "id": "<string, required>",
      "source": "<string, required>",
      "type": "<string, required: topic | hashtag | format | platform_signal>",
      "label": "<string, required>",
      "observed_at": "<string, ISO 8601, required>",
      "metadata": {}
    }
  ]
}
```

| Field              | Type   | Required | Description |
|--------------------|--------|----------|-------------|
| `trends`           | array  | Yes      | List of trend objects. |
| `trends[].id`      | string | Yes      | Unique trend identifier. |
| `trends[].source`  | string | Yes      | Source identifier (e.g. platform or feed name). |
| `trends[].type`    | string | Yes      | One of: `topic`, `hashtag`, `format`, `platform_signal`. |
| `trends[].label`   | string | Yes      | Human-readable label (e.g. topic or hashtag text). |
| `trends[].observed_at` | string | Yes | When this trend was observed (ISO 8601). |
| `trends[].metadata`| object | No       | Source-specific key-value metadata. |

---

## Error conditions

| Code | Condition | Client action |
|------|------------|----------------|
| `400` | Invalid `agent_id`, invalid `since`, or `limit` out of range. | Fix request and retry. |
| `503` | Trend source unavailable. | Retry with backoff. |

Error response body SHOULD include a machine-readable code and an optional human-readable `message`.

---

## Example usage

**Request:**

```json
{
  "agent_id": "chimera-influencer-1",
  "sources": ["twitter", "youtube"],
  "since": "2025-02-01T00:00:00Z",
  "limit": 20
}
```

**Response (success):**

```json
{
  "trends": [
    {
      "id": "trend-abc123",
      "source": "twitter",
      "type": "hashtag",
      "label": "#AITools",
      "observed_at": "2025-02-06T10:00:00Z",
      "metadata": { "volume": 15000 }
    }
  ]
}
```

**Response (error 503):**

```json
{
  "code": "503",
  "message": "Trend source unavailable; retry with backoff."
}
```
