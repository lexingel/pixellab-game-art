# pixellab-game-art

Make pixel-art game assets with [PixelLab](https://pixellab.ai) by talking to your AI assistant -
sprites, backgrounds, buildings, icons, attack animations and effects - with clear steps, the cost
of every job shown up front, and plain-language results. Built for people who have never used
PixelLab before; deep enough to keep using after.

## Pick your version

| You use | Folder |
|---|---|
| **Claude Code** | [`claude-code/`](claude-code/) - slash commands (`/pga-start`, `/pga-char`, …) |
| **Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode** or another agent | [`any-agent/`](any-agent/) - the same skill in the open Agent Skills format |

## Easiest start (about 5 minutes)

**1. Download it.** On this page click the green **Code** button → **Download ZIP**. Then unzip it:
Windows - right-click the ZIP in your Downloads → *Extract All…*; Mac - double-click it. You get a
folder called `pixellab-game-art-main`.

**2. Open your AI assistant inside that folder.** The assistant has to be "in" the folder so it can
read the setup instructions that came with it:

| You use | Do this |
|---|---|
| **Claude desktop app** (Code tab) | Start a new session and choose the `pixellab-game-art-main` folder as the folder to work in. |
| **Claude Code** in a terminal | Open a terminal in the folder (below), type `claude`, press Enter. |
| **Codex CLI** / **Gemini CLI** / **OpenCode** | Open a terminal in the folder (below), type `codex` / `gemini` / `opencode`, press Enter. |
| **Cursor** / **VS Code** (Copilot) | *File → Open Folder…* → pick the folder, then open the chat (agent) panel. |

*Open a terminal in a folder:* **Windows** - open the folder in File Explorer, click the address bar, type
`cmd`, press Enter. **Mac** - right-click the folder in Finder → *New Terminal at Folder*.

**3. Copy this sentence into the assistant's chat and send it:**

> Set up the PixelLab skill for me - follow SETUP_FOR_AI.md.

The assistant reads the instructions file and installs everything itself. It only asks you for three
things: install Python if it's missing, make a free PixelLab account at https://pixellab.ai and copy
your token, and run **one** command it gives you with that token (paste the token into that command
yourself - never into the chat). Then it tells you to restart the assistant.

**4. Make your first art.** Restart the assistant in your game's folder (any folder works) and type
`/pga-init` (pick your art style), then `/pga-start` - a guided first project that explains every step.
On assistants other than Claude Code, type them without the slash: `pga-init`, `pga-start`.

Each folder's README has the manual setup, every command, costs and waits, a glossary, engine import
notes and the privacy note (sharing results with the authors is off unless you turn it on).

## What it does for you

- Turns a short idea into a good PixelLab prompt in your game's style (or one copied from your art).
- Shows each PixelLab call and its cost before it runs; never repeats a paid call.
- Checks results automatically before you see them; explains problems in plain words.
- Remembers several named art styles per project; matches new art to art you approved.
- Picks cheaper AI models for simple steps; works on PixelLab's free trial and every plan.

## Updates

The skill is updated weekly. Already installed? Tell your assistant **`pga-update`** - it downloads
the new version and merges it into your install, keeping any skill file you changed (`pga-update undo`
goes back). Your styles and generated art are never touched.

## Your data: consent first, lessons shared weekly

- **Nothing is sent unless you say yes.** Setup asks once; the answer is off by default. You choose
  `stats` (numbers and settings only) or `prompts` (plus your prompt text), and can preview, switch
  off or delete everything you sent at any time (`/pga-feedback`).
- Never sent: your PixelLab token, images, file paths, uploads or job ids.
- **Every week, what the shared results teach is folded back into the skill for all users** - better
  prompts, safer settings, new pitfall notes. Each weekly [CHANGELOG](CHANGELOG.md) entry lists what changed
  because of shared data and how many shared jobs it came from. Raw records are never published.

Details: the "Privacy" section in each folder's README.

The skill is MIT-licensed ([LICENSE](LICENSE)). Assets you make fall under [PixelLab's terms](https://pixellab.ai/termsofservice). Changes: [CHANGELOG.md](CHANGELOG.md).
