# PixelLab prompt library (distilled from a real game's usage)

Source: ~4,300 generative PixelLab MCP calls made while building a dark-fantasy strategy RPG with
side-view pixel-art battles. Heroes stand on the left facing right; monsters and bosses stand on
the right facing left. Hub screens use painted backdrops with clickable props, and there are a
hamlet of buildings, items and icons, and wide story pictures.

All prompts below come from the log unless marked as a TEMPLATE, lightly edited so names are
generic descriptions. Image inputs, uploads and URLs are shown as `<image>`. Swap the nouns for
your own.

The library is split by asset type so a command reads only what it needs. Always read
`library/house_rules.md` plus the one file for the job:

- `library/house_rules.md` - House rules that apply everywhere (2 KB)
- `library/backgrounds.md` - Battle backgrounds (4 KB)
- `library/scenes.md` - Screen / hub backdrops and story pictures (5 KB)
- `library/buildings.md` - Buildings and hamlet props (4 KB)
- `library/characters.md` - Characters (heroes, monsters, bosses, champions, portraits) (6 KB)
- `library/icons.md` - Items and icons (5 KB)
- `library/ui_tiles.md` - UI assets, tiles and floors (4 KB)
- `library/animation.md` - Animation actions (`animate_image`) (6 KB)
- `library/pose_edits.md` - Pose edits (`edit_image_pro_flash`) (8 KB)
- `library/vfx.md` - VFX (`vfx_workbench`) (7 KB)
