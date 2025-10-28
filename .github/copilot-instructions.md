<!-- Copilot / AI agent instructions for conduit_for_blender -->

This file gives concise, repo-specific guidance to an AI coding assistant so it can be productive immediately.

- Project layout: top-level Python package with these key directories:
  - `operators/` — Blender Operator implementations (e.g. `FILE_OT_LinkTask.py`)
  - `panels/` — Blender UI Panels (e.g. `VIEW3D_PT_UI_Sample.py`)
  - root: `blender_manifest.toml`, `__init__.py`, `constants.py`, `preferences.py`, `README.md`

- Big picture: This repo is a Blender add-on that "connects Conduit and Blender". The add-on reads metadata from
  `blender_manifest.toml` (via `constants.get_manifest()`), exposes operators in `operators/`, and UI panels in `panels/`.

- Naming / patterns to follow (explicit examples):
  - Operator IDs are built with `constants.get_operator(name)` which prefixes `bl_id_prefix` (lowercase). Example: `get_operator("operator")` in `operators/FILE_OT_LinkTask.py`.
  - Panels use `AddonProperties.panel_category` for the UI tab (`panels/VIEW3D_PT_UI_Sample.py`). Don't hardcode the category string.
  - Addon preferences class `Sample_Preferences` sets `bl_idname = __package__` in `preferences.py` — use `__package__` for addon identification.

- How code interacts with Blender & manifest:
  - Manifest is read with `tomllib` in `constants.get_manifest()`; fields like `blender_version_min` and `build.paths_exclude_pattern` are authoritative.
  - To get saved addon preferences, use `constants.get_preferences()` which calls `bpy.context.preferences.addons.get(__package__).preferences`.

-Developer workflows discovered in README:
  - The repository includes a GitHub Action for building and releasing ZIPs for the add-on (keep build artifacts out of releases via `build.paths_exclude_pattern`).

- Important constraints & conventions for edits:
  - Keep `bl_id_prefix` lowercase and centralized in `constants.py`.
  - Prefer `get_operator("name")` when referencing operator IDs in UI code (`layout.operator(get_operator("toggle_server"))`).
  - Use `Connector` from `ConduitConnect` (operators call `Connector().get_asset()` in `FILE_OT_LinkTask.py`) — respect its API (do not assume synchronous network side-effects without checking the connector implementation).

- What to avoid or not change lightly:
  - Do not change `blender_manifest.toml` fields (like `schema_version`, `id`, `blender_version_min`) without verifying compatibility; these are used to build releases.
  - Avoid hardcoding the addon package name; use `__package__` and helpers in `constants.py`.

- Useful file references for specific patterns:
  - `constants.py` — central place for `bl_id_prefix`, `AddonProperties`, manifest & preference helpers.
  - `operators/FILE_OT_LinkTask.py` — example operator showing how `Connector` is used and how `bl_idname` is created.
  - `panels/VIEW3D_PT_UI_Sample.py` — example UI panel using `get_operator` and `AddonProperties.panel_category`.
  - `blender_manifest.toml` — build metadata and packaging rules.

- If asked to extend functionality: prefer adding new operator and panel files under `operators/` and `panels/`, using the established `get_operator` and `AddonProperties` conventions. Add unit-like tests or small scripts externally; note that Blender-specific behavior typically requires running inside Blender.

If you need more granular developer commands (local build commands, exact GitHub Action names, or how to run tests in CI), ask me and I will open the relevant workflow file or provide the exact command sequence.

---
Please review this draft and tell me any missing workflows, commands, or conventions you'd like included (for example: exact build/release steps, CI job names, or the `ConduitConnect` API surface).
