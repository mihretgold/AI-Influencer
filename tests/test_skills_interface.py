"""
Test skills/ interface contracts per specs/technical.md and skills/*/README.md.

PLACEHOLDER: No production implementation. Skill invokers are stubbed below.
Failures are expected for test_skill_*_integration_returns_schema tests until
each skill is implemented. Contract tests validate declared inputs, output schema,
and error contracts.
"""

import pytest
from pathlib import Path

# --- Declared contracts from specs / skills (no implementation) ---
SKILL_FETCH_TRENDS_REQUIRED_INPUTS = {"agent_id"}
SKILL_FETCH_TRENDS_OPTIONAL_INPUTS = {"sources", "since", "limit"}
SKILL_FETCH_TRENDS_OUTPUT_KEYS = {"trends"}
SKILL_FETCH_TRENDS_TREND_KEYS = {"id", "source", "type", "label", "observed_at"}
SKILL_FETCH_TRENDS_ERROR_CODES = {"400", "503"}

SKILL_GENERATE_VIDEO_REQUIRED_INPUTS = {"agent_id", "slot_id", "content_type", "platform"}
SKILL_GENERATE_VIDEO_OPTIONAL_INPUTS = {"topic", "constraints", "context_refs"}
SKILL_GENERATE_VIDEO_OUTPUT_KEYS = {"content_id", "slot_id", "body", "evaluation_pending"}
SKILL_GENERATE_VIDEO_ERROR_CODES = {"400", "422", "503"}

SKILL_PUBLISH_CONTENT_REQUIRED_INPUTS = {"content_id", "agent_id", "platform"}
SKILL_PUBLISH_CONTENT_OPTIONAL_INPUTS = {"scheduled_at", "idempotency_key"}
SKILL_PUBLISH_CONTENT_OUTPUT_KEYS = {"publish_id", "content_id", "platform", "status"}
SKILL_PUBLISH_CONTENT_ERROR_CODES = {"400", "404", "409", "422", "429", "503"}

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


# --- PLACEHOLDER invokers: not implemented; failures expected until skills exist ---
def skill_fetch_trends(agent_id: str, sources=None, since=None, limit=None) -> dict:
    """Placeholder. See skills/skill_fetch_trends/README.md."""
    raise NotImplementedError("skill_fetch_trends not implemented")


def skill_generate_video(
    agent_id: str,
    slot_id: str,
    content_type: str,
    platform: str,
    topic=None,
    constraints=None,
    context_refs=None,
) -> dict:
    """Placeholder. See skills/skill_generate_video/README.md."""
    raise NotImplementedError("skill_generate_video not implemented")


def skill_publish_content(
    content_id: str,
    agent_id: str,
    platform: str,
    scheduled_at=None,
    idempotency_key=None,
) -> dict:
    """Placeholder. See skills/skill_publish_content/README.md."""
    raise NotImplementedError("skill_publish_content not implemented")


# --- skill_fetch_trends ---


def test_skill_fetch_trends_accepts_correct_input_parameters() -> None:
    """Skill fetch_trends MUST accept agent_id (required) and optional sources, since, limit."""
    # Assert declared contract: required and optional params are defined
    assert SKILL_FETCH_TRENDS_REQUIRED_INPUTS == {"agent_id"}
    assert "sources" in SKILL_FETCH_TRENDS_OPTIONAL_INPUTS
    assert "since" in SKILL_FETCH_TRENDS_OPTIONAL_INPUTS
    assert "limit" in SKILL_FETCH_TRENDS_OPTIONAL_INPUTS


def test_skill_fetch_trends_returns_data_matching_declared_output_schema() -> None:
    """Skill fetch_trends output MUST have 'trends' and each trend MUST have declared fields."""
    sample = {
        "trends": [
            {
                "id": "t1",
                "source": "twitter",
                "type": "hashtag",
                "label": "#X",
                "observed_at": "2025-02-06T00:00:00Z",
            }
        ]
    }
    assert SKILL_FETCH_TRENDS_OUTPUT_KEYS.issubset(sample.keys())
    for trend in sample["trends"]:
        assert SKILL_FETCH_TRENDS_TREND_KEYS.issubset(trend.keys())


def test_skill_fetch_trends_exposes_explicit_error_contract() -> None:
    """Skill fetch_trends MUST declare error codes 400, 503."""
    assert SKILL_FETCH_TRENDS_ERROR_CODES == {"400", "503"}
    # Contract is also documented in skill README
    readme = SKILLS_DIR / "skill_fetch_trends" / "README.md"
    assert readme.exists()
    text = readme.read_text()
    assert "400" in text and "503" in text


@pytest.mark.xfail(strict=False, reason="Placeholder not implemented; see skills/skill_fetch_trends/README.md")
def test_skill_fetch_trends_integration_returns_schema() -> None:
    """Calling skill_fetch_trends MUST return output matching declared schema. Remove xfail when implemented."""
    result = skill_fetch_trends("agent-1")
    assert SKILL_FETCH_TRENDS_OUTPUT_KEYS.issubset(result.keys())
    for trend in result["trends"]:
        assert SKILL_FETCH_TRENDS_TREND_KEYS.issubset(trend.keys())


# --- skill_generate_video ---


def test_skill_generate_video_accepts_correct_input_parameters() -> None:
    """Skill generate_video MUST accept agent_id, slot_id, content_type, platform (required)."""
    assert SKILL_GENERATE_VIDEO_REQUIRED_INPUTS == {
        "agent_id",
        "slot_id",
        "content_type",
        "platform",
    }
    assert "topic" in SKILL_GENERATE_VIDEO_OPTIONAL_INPUTS


def test_skill_generate_video_returns_data_matching_declared_output_schema() -> None:
    """Skill generate_video output MUST have content_id, slot_id, body, evaluation_pending."""
    sample = {
        "content_id": "draft-1",
        "slot_id": "slot-1",
        "body": {"text": "", "media_uri": "storage://x", "metadata": {}},
        "evaluation_pending": True,
    }
    assert SKILL_GENERATE_VIDEO_OUTPUT_KEYS.issubset(sample.keys())


def test_skill_generate_video_exposes_explicit_error_contract() -> None:
    """Skill generate_video MUST declare error codes 400, 422, 503."""
    assert SKILL_GENERATE_VIDEO_ERROR_CODES == {"400", "422", "503"}
    readme = SKILLS_DIR / "skill_generate_video" / "README.md"
    assert readme.exists()
    text = readme.read_text()
    assert "400" in text and "422" in text and "503" in text


@pytest.mark.xfail(strict=False, reason="Placeholder not implemented; see skills/skill_generate_video/README.md")
def test_skill_generate_video_integration_returns_schema() -> None:
    """Calling skill_generate_video MUST return output matching schema. Remove xfail when implemented."""
    result = skill_generate_video(
        agent_id="a1", slot_id="s1", content_type="video", platform="youtube"
    )
    assert SKILL_GENERATE_VIDEO_OUTPUT_KEYS.issubset(result.keys())


# --- skill_publish_content ---


def test_skill_publish_content_accepts_correct_input_parameters() -> None:
    """Skill publish_content MUST accept content_id, agent_id, platform (required)."""
    assert SKILL_PUBLISH_CONTENT_REQUIRED_INPUTS == {
        "content_id",
        "agent_id",
        "platform",
    }
    assert "idempotency_key" in SKILL_PUBLISH_CONTENT_OPTIONAL_INPUTS


def test_skill_publish_content_returns_data_matching_declared_output_schema() -> None:
    """Skill publish_content output MUST have publish_id, content_id, platform, status."""
    sample = {
        "publish_id": "pub-1",
        "content_id": "draft-1",
        "platform": "youtube",
        "status": "published",
    }
    assert SKILL_PUBLISH_CONTENT_OUTPUT_KEYS.issubset(sample.keys())


def test_skill_publish_content_exposes_explicit_error_contract() -> None:
    """Skill publish_content MUST declare error codes 400, 404, 409, 422, 429, 503."""
    assert SKILL_PUBLISH_CONTENT_ERROR_CODES == {
        "400",
        "404",
        "409",
        "422",
        "429",
        "503",
    }
    readme = SKILLS_DIR / "skill_publish_content" / "README.md"
    assert readme.exists()
    text = readme.read_text()
    for code in SKILL_PUBLISH_CONTENT_ERROR_CODES:
        assert code in text


@pytest.mark.xfail(strict=False, reason="Placeholder not implemented; see skills/skill_publish_content/README.md")
def test_skill_publish_content_integration_returns_schema() -> None:
    """Calling skill_publish_content MUST return output matching schema. Remove xfail when implemented."""
    result = skill_publish_content(
        content_id="draft-1", agent_id="a1", platform="youtube"
    )
    assert SKILL_PUBLISH_CONTENT_OUTPUT_KEYS.issubset(result.keys())
