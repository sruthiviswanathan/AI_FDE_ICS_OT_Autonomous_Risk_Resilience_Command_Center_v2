# Command Center (APP)

Synthetic, read-only operator surface. **No live OT.** Fixtures are CSV slices, not a second system of record.

Generate (or regenerate) the demo bundle:

```bash
PYTHONPATH=src python scripts/generate_command_center_fixtures.py
```

Output: `apps/command_center/fixtures/command_center_fixtures.json`.

APP-02 builds the UI. This increment does not add isolate-execute or PLC write controls.
