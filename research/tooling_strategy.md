# Project Chimera — Tooling Strategy

**Document type:** Strategy for developer and runtime tooling  
**Audience:** Platform engineers, AI agents (IDE), operators  
**Scope:** Developer tools (MCP and IDE); runtime agent skills are defined in `skills/`.

This document defines **which tools** support development of Chimera and **why** they were chosen. It is a tooling strategy, not a step-by-step tutorial.

---

## 1. Guiding principles

- **Spec compliance:** Tools must not encourage or enable behavior that bypasses `specs/`. The IDE agent MUST check specs before generating code; tooling should support traceability (e.g. linking changes to spec sections).
- **Safety:** Tools that modify state (git, filesystem, publish) must be used in a way that supports audit, rollback, and human oversight where required.
- **Speed and correctness:** Automation (lint, format, test, MCP-aided edits) reduces drift and speeds up feedback; tooling choices should favor reproducibility and explicit contracts.

---

## 2. Selected MCP servers (developer)

The following MCP servers are recommended for use by the **developer** (and the IDE’s AI agent) when working in the Chimera repository. Configuration lives in `.cursor/mcp.json` or the IDE’s MCP settings.

### 2.1 Git MCP (e.g. `@modelcontextprotocol/server-git` or equivalent)

**What it enables:**

- Read git status, diff, log, and branch information from within the IDE.
- Stage, commit, and optionally push with explicit messages, without leaving the editor.
- Compare branches and inspect history for traceability.

**Why chosen:**

- **Traceability:** Every change can be tied to a commit and, by convention, to a spec reference or ticket. Supports “plan first, then implement, then commit with clear message.”
- **Safety:** Reduces ad-hoc terminal git usage; the agent can propose commits that reference `specs/` or task IDs. Rollback and blame remain possible.
- **Correctness:** Ensures the agent sees the current repo state (dirty files, current branch) before suggesting edits, reducing invalid or conflicting changes.

**Improves:** Traceability (spec → code → commit); safety (audit trail); speed (no context-switch to terminal for simple git ops).

---

### 2.2 Filesystem MCP (e.g. `@modelcontextprotocol/server-filesystem` or equivalent)

**What it enables:**

- Read and write files under allowed paths (e.g. project root, `src/`, `specs/`, `tests/`) with explicit paths.
- List directories and check existence before creating or modifying files.
- Enforce scope so that the agent cannot touch paths outside the project (e.g. system or home dirs).

**Why chosen:**

- **Safety:** Scoped filesystem access prevents accidental or malicious writes outside the repo. Essential when the IDE agent creates or edits many files.
- **Correctness:** The agent can verify “file X exists” or “directory Y structure” before proposing edits, aligning with the plan-first rule in `.cursor/rules/chimera.mdc`.
- **Speed:** Single interface for read/write/list instead of mixing terminal commands and editor buffers; reduces errors from path mistakes.

**Improves:** Safety (scope); correctness (explicit paths and existence checks); speed (structured file ops).

---

### 2.3 Tenx Feedback / Analytics MCP (existing: `tenxfeedbackanalytics`)

**What it enables:**

- Log trigger events (e.g. task completion, passage time) for fluency and performance tracking.
- Receive analysis feedback (e.g. summaries, improvement suggestions, statistics) to improve assistance quality.

**Why chosen:**

- **Correctness:** Feedback loops help the agent and the user notice incomplete or off-spec work and correct it.
- **Quality:** Encourages “verify then deliver” and surfaces metrics that support iterative improvement of both prompts and agent behavior.

**Improves:** Correctness (feedback on output); quality (metrics and suggestions). Already configured in `.cursor/mcp.json`.

---

### 2.4 Optional: Database / API MCP (future)

For later phases, an MCP server that exposes **read-only** access to development or staging data (e.g. sample trends, content drafts, publish records) could support:

- **Correctness:** The agent could validate responses against real schema and sample data without running full stacks.
- **Safety:** Read-only keeps the agent from mutating shared data; writes remain through defined APIs and pipelines.

Not required for Task 2.3; document when/if introduced.

---

## 3. IDE and local tooling (non-MCP)

- **uv:** Package and environment management. Use `uv sync`, `uv run`, and lockfile for reproducible builds (see `README.md` and `pyproject.toml`).
- **Ruff:** Lint and format. Ensures style and static checks align with project standards; run before commit.
- **Pytest:** Tests. Required for verifying that implementation matches `specs/technical.md` contracts and user stories.
- **Cursor rules:** `.cursor/rules/chimera.mdc` enforces spec precedence and plan-first behavior; the IDE agent MUST follow it.

These are not MCP servers but are part of the same strategy: reproducible env, fast feedback, and spec-aligned behavior.

---

## 4. Summary

| Tool / MCP           | Role        | Improves                          |
|----------------------|------------|------------------------------------|
| Git MCP              | Version control, traceability | Safety, traceability, speed |
| Filesystem MCP       | Scoped file read/write       | Safety, correctness, speed |
| Tenx Feedback MCP   | Logging and analysis feedback| Correctness, quality        |
| uv / Ruff / Pytest   | Env, lint, test             | Reproducibility, correctness |

New MCP servers or tools should be evaluated against: (1) spec compliance, (2) safety and audit, (3) impact on speed and correctness. This file should be updated when the tool set changes.
