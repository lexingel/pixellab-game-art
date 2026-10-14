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

## Easiest start

1. Download this repository (green **Code** button → *Download ZIP*, then unzip) or `git clone` it.
2. Open your AI assistant in the downloaded folder and say:
   **"Set up the PixelLab skill for me - follow SETUP_FOR_AI.md."**
3. It installs everything and checks it. You only install Python if it's missing, get your PixelLab
   token (free account at https://pixellab.ai) and run one command with it.
4. Say `/pga-init` (your art style), then `/pga-start` - a guided first project that explains every step.

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
