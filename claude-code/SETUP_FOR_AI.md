# Setting up the PixelLab game-art skill - instructions for the AI assistant

The user asked you to set this skill up. Do the work yourself; ask the user only for what you
cannot do (installing Python, running one command that contains their token, restarting you).
Keep each message short and plain - the user may be brand new to PixelLab, Python and terminals.

1. **Which agent are you?** Claude Code, Codex, Gemini CLI, Cursor, VS Code / GitHub Copilot,
   OpenCode or another. You need this for steps 3 and 4.
2. **Python.** Run `python --version` (then `python3 --version`, then `py --version` on Windows).
   None works → tell the user: "Install Python from https://www.python.org/downloads/ (on Windows tick
   *Add Python to PATH*), then tell me when it's done." Wait for them.
3. **Install.** In this folder run, with the Python command that worked:
   - Claude Code bundle (`pixellab-skills`): `python install.py --pip`
   - Other agents (`pixellab-agent-skill`): `python install.py --pip --agent <codex|gemini|cursor|opencode|copilot>`
   Read the output. If pip is blocked ("externally-managed-environment"), use the option it prints for
   this computer; ask the user before anything with `sudo` or `--break-system-packages`.
4. **Connect PixelLab.** Check whether a `pixellab` MCP server is already configured (Claude Code:
   `claude mcp list`; Codex: `codex mcp list`; Gemini CLI: `~/.gemini/settings.json`; Cursor:
   `~/.cursor/mcp.json`; VS Code: `.vscode/mcp.json`; OpenCode: `opencode.json`). If it isn't:
   - Tell the user: "Get your PixelLab token at https://api.pixellab.ai/mcp - sign in, or make a free
     account at https://pixellab.ai first." **Never ask them to paste the token into the chat.**
   - Claude Code: give them exactly this to run in their own terminal, with their token in place of
     YOUR_TOKEN:
     `claude mcp add --transport http --scope user pixellab https://api.pixellab.ai/mcp --header "Authorization: Bearer YOUR_TOKEN"`
   - Other agents: add the `pixellab` entry to the config file yourself, exactly as the README's
     "Connect PixelLab" table shows (it reads the token from the `PIXELLAB_TOKEN` environment
     variable; merge it into any existing servers block, don't overwrite the file). Then give them the
     one command that stores the token - Windows: `setx PIXELLAB_TOKEN "YOUR_TOKEN"`; macOS / Linux:
     `echo 'export PIXELLAB_TOKEN=YOUR_TOKEN' >> ~/.zshrc` (or `~/.bashrc`).
5. **Restart.** Ask them to close and reopen you in their game's folder (a new terminal too, if they
   stored the token in an environment variable), then say `pga-doctor` (`/pga-doctor` in Claude Code).
   The doctor checks the connection, plan, balance, Python and packages, and prints any fix.
6. **Done.** Tell them: "Everything works. Say `/pga-init` to pick your art style, then `/pga-start`
   for a guided first project - about 15-20 generations, with an explanation at every step."
