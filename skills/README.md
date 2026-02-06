# Project Chimera — Runtime skills

**Definition:** A **skill** is a self-contained capability package with a clear input/output contract. Skills are used by Chimera agents at runtime. This directory holds **contracts and structure only** — no implementation code.

**Spec reference:** `specs/technical.md` (API contracts), `specs/functional.md` (user stories).

---

## Directory structure

```
skills/
├── README.md                    # This index
├── skill_fetch_trends/
│   └── README.md                # Trend discovery contract
├── skill_generate_video/
│   └── README.md                # Video (and text-and-video) generation contract
└── skill_publish_content/
    └── README.md                # Publish approved content to platform
```

---

## Skill index

| Skill | Purpose | Spec |
|-------|---------|------|
| **skill_fetch_trends** | Return trend signals for content planning. | technical.md § A.1 |
| **skill_generate_video** | Generate video (or text-and-video) for a plan slot. | technical.md § A.2 |
| **skill_publish_content** | Publish approved content draft to a platform. | technical.md § A.4 |

Each skill README defines: **Purpose**, **Inputs (JSON schema)**, **Outputs (JSON schema)**, **Error conditions**, **Example usage**. Implementation lives outside this directory and MUST conform to these contracts.

---

## Adding or changing skills

- New skills MUST have a folder and a README.md with the same sections as above.
- Contract changes MUST align with `specs/technical.md`; if the spec changes, update the skill README and vice versa (spec has precedence).
- Do not add implementation code to `skills/`; keep this directory contracts-only.
