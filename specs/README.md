# Project Chimera — Specifications index

This directory is the **source of truth** for Project Chimera. AI agents and developers must treat these documents as authoritative.

## Directory structure

```
specs/
├── README.md                 # This index
├── _meta.md                  # Vision, non-goals, constraints, success criteria
├── functional.md             # Agent-centered user stories (what the system must do)
├── technical.md              # API contracts (JSON schemas) and database ERD
└── openclaw_integration.md   # OpenClaw / agent network integration
```

## Document roles

| File | Purpose |
|------|---------|
| **_meta.md** | Constitution: vision, non-goals, core constraints, success criteria. |
| **functional.md** | User stories in the form "As an Agent, I need to ___ so that ___." No implementation. |
| **technical.md** | Input/output contracts for key actions; conceptual ERD for agents, content, publishing, trends, memory, audit. |
| **openclaw_integration.md** | How Chimera advertises itself and integrates with OpenClaw (or similar) agent networks. |

## Rules

- **Do not implement** in this directory; specs describe *what*, not *how*.
- **Write for AI agents** as primary audience: precise, explicit, no implicit intent.
- **Change control:** Updates to _meta.md and major contract changes should be explicit and ratified.
