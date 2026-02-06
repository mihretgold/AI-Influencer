# Project Chimera

Production-grade AI agent system. Task 1.3: Golden environment with **uv**, structured deps, and Tenx MCP Sense integration.

## Requirements

- **Python** ≥ 3.12
- **uv** — [install](https://docs.astral.sh/uv/getting-started/installation/)

## Quick start

```bash
# Clone (if applicable) and enter project root
cd "AI Influencer"

# Create venv, install deps, lock (reproducible)
uv sync --all-groups

# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format .
```

## Project layout

```
.
├── .cursor/           # Cursor IDE (agents, commands, MCP config)
├── src/chimera/       # Main package
├── tests/
├── pyproject.toml     # Deps, tool config, uv settings
├── uv.lock            # Lockfile (commit for reproducibility)
└── README.md
```

## Dependency groups (uv)

| Group   | Purpose              | Install / use                          |
|---------|----------------------|----------------------------------------|
| (core)  | Runtime dependencies  | Always installed with `uv sync`        |
| **dev** | Testing, lint, format| `uv sync --group dev` or default-groups|
| **tools** | MCP / tooling      | `uv sync --group tools`                |

Full dev + tools: `uv sync --all-groups`.

## Tenx MCP Sense — confirm and log connection

MCP is configured in **`.cursor/mcp.json`** (server: `tenxfeedbackanalytics` / Tenx MCP Pulse).

### 1. Confirm connection from the IDE

1. **Cursor Settings → MCP**
   - Open Cursor Settings (e.g. `Ctrl+,`), search for **MCP**.
   - Ensure the **tenxfeedbackanalytics** (or **tenxanalysismcp**) server is **Enabled** and shows a green/connected state.

2. **Composer / Chat**
   - In a Cursor Composer or Chat session, check the **MCP / Tools** section.
   - You should see tools provided by **tenxfeedbackanalytics** (e.g. feedback or analytics tools). If they appear and are callable, the connection is working.

3. **Manual tool check**
   - Type a prompt that clearly requires a Tenx tool (e.g. “Use the Tenx feedback tool to…”).
   - If the model can invoke the tool and return a result, the connection is successful.

### 2. Log a successful connection

- **Where to log**
  - In this repo: add a short note to **`docs/MCP_SENSE_VERIFICATION.md`** (see below) with:
    - **Date**
    - **IDE**: Cursor
    - **MCP server**: tenxfeedbackanalytics (mcppulse.10academy.org)
    - **Result**: e.g. “Tools visible in Composer; [tool name] invoked successfully.”

- **Optional**
  - In Cursor, you can capture a screenshot of the MCP settings page showing the server enabled, or of Composer showing the Tenx tools, and store it in `docs/` or attach to the verification doc.

Detailed steps and a verification checklist live in **`docs/MCP_SENSE_VERIFICATION.md`**.

## Lint and format

```bash
uv run ruff check .
uv run ruff format .
```

## Tests

```bash
uv run pytest
# With coverage
uv run pytest --cov=chimera --cov-report=term-missing
```

## License

MIT
