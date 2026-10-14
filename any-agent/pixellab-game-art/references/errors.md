# When something goes wrong - plain-language explanations

Read this when a PixelLab call, a download or a script fails. Tell the user, in one or two plain
sentences, what happened and what you are doing about it (or the one thing they need to do). No
error codes unless they ask; never blame them; never apologise at length.

| What you see | Say (plain words) | Do |
|---|---|---|
| No PixelLab tools / "server not connected" | "PixelLab isn't connected to me yet." | Show the connect step for this agent (prompt_improver.md §0) or suggest `pga-doctor`. |
| Auth error, 401, "invalid token" | "PixelLab didn't accept the token - it may be mistyped or expired." | Get a new token at https://api.pixellab.ai/mcp and re-add the server. |
| Balance 0 / "insufficient generations" | "You're out of PixelLab generations for this month (they refill on <reset date>)." | Offer what's free: `--dry`, `pga-prompt`, `pga-vfx`; or adding credits at pixellab.ai. |
| "Tier 1 required" / a tool refused for the plan | "That tool needs a higher PixelLab plan, so I'm using <fallback> instead." | Switch to the fallback (pixellab_api.md → Subscription tiers); no question. |
| Job `FAILED` / 410 / "stalled" | "PixelLab dropped that job - it's refunded, so it cost nothing. Trying it once more." | Resubmit once; a second failure → say so and suggest trying later. |
| `TIMEOUT … still running` | "Still drawing - PixelLab takes about <time> for this. Checking again." | Run the same fetch.py command again. Not an error. |
| Upload failed / image too big | "That image is too big for this tool (<size>; it takes up to 256 px)." | Shrink a copy (`pad_sprite.py` / any editor) or use a smaller crop. |
| Python / package missing | "A helper needs <package>, which isn't installed yet." | Give the exact install line from `check_setup.py`; generation still works without it. |
| QA flagged the result | "It came out <with a stray flash / cropped / facing the wrong way>; <fixed it / re-drawing it once>." | Hard defects re-roll once (prompt_improver §8); otherwise say what to change. |
| Rate limit / 429 / too many jobs | "PixelLab is busy with your other jobs - sending the rest as they finish." | Submit up to the tier's limit, then the rest. |
| Anything else | "PixelLab returned an error I don't recognise: <one-line message>." | Suggest `pga-doctor`; offer to retry once. |
