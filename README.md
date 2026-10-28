# Pixtorium MCP

Let an AI agent edit your photos in [Pixtorium](https://pixtorium.com), an
image editor for Windows, macOS and Linux. The agent works on the pictures you
have open, one step at a time, while you watch. Every step lands in History and
can be undone.

Pixtorium is proprietary software and is not in this repository. This
repository is the reference for its MCP server: how to connect, what the tools
do, and the full list of image operations.

- 22 tools: open, look, select, apply, layers, looks, undo, save.
- 134 image operations: light, white balance, color mixer, curves, noise
  reduction, sharpening, blur, retouching, distortions, artistic filters.
- Everything runs on your computer. The server listens on `127.0.0.1` only.

## Connect

Start Pixtorium and turn on **Agents › Let AI agents edit**. The menu shows the
address, `http://127.0.0.1:8737/mcp` by default, and has a **Connect** section
with one entry per agent. Or start the editor with `pixtorium --agents`.

| Agent | How |
|---|---|
| Claude Code | `claude mcp add -s user --transport http pixtorium http://127.0.0.1:8737/mcp` |
| Codex (CLI, IDE extension, app) | `codex mcp add pixtorium --url http://127.0.0.1:8737/mcp` |
| Claude Desktop | **Agents › Add to Claude Desktop** in Pixtorium, then restart Claude Desktop |
| Any other MCP client | the HTTP endpoint at the address above, or stdio through the bridge below |

Use the port the **Agents** menu shows if it is not 8737.

### Clients that only speak stdio

`pixtorium-mcp --connect URL` ships beside the editor and relays stdio to the
running editor. Claude Desktop uses it:

```json
{
  "mcpServers": {
    "pixtorium": {
      "command": "/path/to/pixtorium-mcp",
      "args": ["--connect", "http://127.0.0.1:8737/mcp"]
    }
  }
}
```

If the editor is not running, or **Let AI agents edit** is off, each request
gets an error saying so.

### Headless

`pixtorium-mcp` with no arguments is the same engine without a window, over
stdio. It has no panels, so `show_panel` and the editor's own history view are
not available. Use it for scripts and batch work.

ChatGPT connects only to servers on the internet, so it cannot reach a local
editor.

## What an agent can do

Ask in plain words:

- "Open `holiday.jpg`, make the sky deeper without touching the people, and
  save a copy for the web at 1600 pixels."
- "This photo is too warm. Fix the white balance, check the highlights, and
  tell me what you changed."
- "Remove the bin on the right, and then apply a Golden hour look at 60%."
- "Open every photo in this folder, straighten the horizons and export
  JPEGs."

The server's built-in instructions teach the agent the loop: open, look, select
the area, apply, look again, undo what it does not like, save. It can find
objects in a picture with a labeled grid, so it can select "the thing in cells
F2 and F3".

## Tools

| Tool | What it does |
|---|---|
| `open_image`, `new_image`, `list_images`, `close_image` | Work with open pictures. |
| `view_image` | A preview of the picture or a region, optionally with a labeled ruler. The selection is shown by dimming the rest. |
| `image_info` | Size, selection, history, and tonal statistics: mean color, luminance percentiles, clipping. |
| `pick_color` | The color of one pixel. |
| `select` | Rectangle, ellipse, polygon, color range, main subject, object (by grid cells, box or points), linear and radial gradients, with feathering. |
| `apply` | Applies one of the 134 operations to the selection, or to the whole picture. |
| `list_operations` | Every operation with its parameters, ranges and defaults. |
| `layers`, `layer` | Pixel, text and adjustment layers, masks, blend modes. Reads Lightroom presets (`.xmp`) as adjustment layers. |
| `looks` | One-click looks at any strength, added as adjustment layers so they stay editable. |
| `split_channels` | Splits RGB, HSV or CMY into grayscale pictures to work on separately. |
| `generate_material`, `generate_place` | Hand an area and its mask to your own picture model, and put the result back as a masked layer. |
| `macro` | List, play and batch-run recorded macros. |
| `lesson` | Teach a person to fix a photo, with a practice picture and a check of their result. |
| `show_panel` | Open an operation in the editor with a live preview for the person to fine-tune. |
| `undo`, `redo` | Step back and forward, selection changes included. |
| `save_image` | PNG, JPEG, WebP, TIFF, BMP, GIF, TGA, PCX, or OpenRaster (`.ora`) with layers. Can export a resized copy with quality and sharpening. |

The complete schemas are in [`tools.json`](tools.json), and every operation is
in [`operations.json`](operations.json). Both are generated from the server
itself with [`scripts/update_reference.py`](scripts/update_reference.py), so
they cannot drift from the real thing. They match Pixtorium 0.5.4; your
install's `list_operations` is authoritative for the version you run.

## Privacy

The server accepts connections from this computer only. Nothing is exposed to
the internet and no account is needed. Pictures stay on your machine unless
your agent sends them to its own model, which is how agents work; that is the
agent's setting, not Pixtorium's.

## Links

- Site and web editor: <https://pixtorium.com>
- Questions or problems with the MCP server: open an issue here.

Documentation © 2026 Igor Plotnikov, MIT license. Development sponsored by
Yovico, Inc.
