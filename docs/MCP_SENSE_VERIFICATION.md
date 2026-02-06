# Tenx MCP Sense — verification and logging

This doc explains how to **confirm** and **log** a successful connection to Tenx MCP Sense (Tenx MCP Pulse) from the Cursor IDE.

## Prerequisites

- Cursor IDE with MCP support.
- Project MCP config: **`.cursor/mcp.json`** should define the `tenxfeedbackanalytics` server pointing at `https://mcppulse.10academy.org/proxy` with headers `X-Device` and `X-Coding-Tool`.

## Step 1: Confirm connection in the IDE

### A. MCP settings

1. Open **Cursor Settings** (`Ctrl+,` or `Cmd+,`).
2. Search for **MCP** (or open **Features → MCP**).
3. Find the server **tenxfeedbackanalytics** (or **tenxanalysismcp**).
4. Confirm it is **Enabled** and shows a **connected** (e.g. green) state.  
   - If it shows an error, check the URL and headers in `.cursor/mcp.json` and your network.

### B. Composer / Chat tools

1. Open **Composer** or a **Chat** session in Cursor.
2. In the panel where tools are listed (e.g. “Tools” or “MCP”), check that tools from **tenxfeedbackanalytics** appear.
3. Run a prompt that clearly requires a Tenx tool (e.g. “Use the Tenx feedback/analytics tool to…”).
4. If the model can **invoke** the tool and you get a **valid response**, the connection is working.

### C. Quick checklist

- [ ] MCP server **tenxfeedbackanalytics** is enabled in Cursor Settings.
- [ ] Server status is connected (no error in UI).
- [ ] At least one Tenx tool is visible in Composer/Chat.
- [ ] A test invocation of that tool succeeds.

## Step 2: Log a successful connection

After a successful verification, add an entry below so the team has a record.

### Log entry template

Copy the block below, fill it in, and append it under **Verification log**.

```markdown
### YYYY-MM-DD — [Your name or “IDE check”]

- **IDE:** Cursor
- **MCP server:** tenxfeedbackanalytics (mcppulse.10academy.org)
- **Result:** [e.g. “Tools visible in Composer; tool X invoked successfully.”]
- **Notes:** [optional]
```

### Verification log

*(Add new entries here.)*

---

*Last updated: 2025-02-06 — Template and checklist added.*
