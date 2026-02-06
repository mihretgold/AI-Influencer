# Skill: Generate Video

**Spec reference:** `specs/technical.md` § A.2 (generate_content), scoped to video and text-and-video.  
**Type:** Runtime agent skill — no implementation in this repo; contract only.

---

## Purpose

Request generation of video content (and optional accompanying text) for a content plan slot. The skill defines the input/output contract for video (and `text_and_video`) generation; it does not implement the generator. Output is a content draft that MUST be evaluated before publish per specs.

---

## Inputs (JSON schema)

Request body MUST be valid JSON with the following shape.

```json
{
  "agent_id": "<string, required>",
  "slot_id": "<string, required>",
  "content_type": "video | text_and_video",
  "topic": "<string, optional>",
  "platform": "<string, required>",
  "constraints": {
    "max_text_length": "<integer, optional>",
    "required_disclosures": ["<string>"],
    "prohibited_topics": ["<string>"],
    "aspect_ratio": "<string, optional>"
  },
  "context_refs": ["<string>"]
}
```

| Field          | Type    | Required | Description |
|----------------|---------|----------|-------------|
| `agent_id`     | string  | Yes      | Agent requesting generation. |
| `slot_id`      | string  | Yes      | Content plan slot this generation fulfills. |
| `content_type` | string  | Yes      | Either `video` or `text_and_video`. |
| `topic`        | string  | No       | Topic or trend label to align with. |
| `platform`     | string  | Yes      | Target platform (for format constraints). |
| `constraints`  | object  | No       | See sub-schema below. |
| `context_refs` | string[]| No       | Optional memory or content IDs to use as context. |

**constraints (optional):**

| Field                 | Type    | Description |
|-----------------------|---------|-------------|
| `max_text_length`     | integer | Max characters for captions/titles. |
| `required_disclosures`| string[]| e.g. `["AI-generated"]`. |
| `prohibited_topics`   | string[]| Topics to avoid. |
| `aspect_ratio`        | string  | For video (e.g. `"16:9"`, `"9:16"`). |

---

## Outputs (JSON schema)

Success response:

```json
{
  "content_id": "<string, required>",
  "slot_id": "<string, required>",
  "body": {
    "text": "<string, optional>",
    "media_uri": "<string, required for video>",
    "metadata": {}
  },
  "evaluation_pending": true
}
```

| Field                 | Type    | Required | Description |
|-----------------------|---------|----------|-------------|
| `content_id`          | string  | Yes      | Internal content draft identifier. |
| `slot_id`             | string  | Yes      | Echo of request `slot_id`. |
| `body`                | object  | Yes      | Type-specific payload. |
| `body.text`           | string  | If text requested | Caption, script, or title. |
| `body.media_uri`      | string  | Yes (for video) | Reference to generated video (URL or storage id). |
| `body.metadata`       | object  | No       | Format, dimensions, duration, etc. |
| `evaluation_pending`  | boolean | Yes      | MUST be `true`; content must be evaluated before publish. |

---

## Error conditions

| Code | Condition | Client action |
|------|------------|----------------|
| `400` | Invalid `agent_id`, `slot_id`, `content_type`, or `platform`. | Fix request and retry. |
| `422` | Generation failed (e.g. safety filter, unsupported format). | Inspect error body; do not retry same payload without change. |
| `503` | Generator unavailable. | Retry with backoff. |

Error response body SHOULD include a machine-readable code and an optional human-readable `message` or `details`.

---

## Example usage

**Request:**

```json
{
  "agent_id": "chimera-influencer-1",
  "slot_id": "slot-xyz-001",
  "content_type": "text_and_video",
  "topic": "#AITools",
  "platform": "youtube",
  "constraints": {
    "max_text_length": 5000,
    "required_disclosures": ["AI-generated"],
    "aspect_ratio": "16:9"
  }
}
```

**Response (success):**

```json
{
  "content_id": "draft-video-abc123",
  "slot_id": "slot-xyz-001",
  "body": {
    "text": "Title: Top 5 AI Tools in 2025\n\nScript: ...",
    "media_uri": "storage://chimera/drafts/draft-video-abc123.mp4",
    "metadata": { "duration_seconds": 180, "resolution": "1920x1080" }
  },
  "evaluation_pending": true
}
```

**Response (error 422):**

```json
{
  "code": "422",
  "message": "Generation failed",
  "details": "Safety filter rejected generated script."
}
```
