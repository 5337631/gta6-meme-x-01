[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/5337631/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/5337631/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

# gta6-meme-x-01 — GTA VI download meme

Entry for the make.fun bounty **gta6-meme-x-01** ("Post a GTA 6 meme on X", $500, top 50 share).

## The meme

![GTA VI download meme](meme.png)

**The joke:** We waited 13 years for GTA VI — and the download needs 3 more days.
The gamer has fallen asleep on the couch in Leonida (neon palms, Vice City glow
outside the window) while the TV sits at a barely-started progress bar. Sitting
on the WiFi router is make.fun's ghost mascot — white ghost, thick black outline,
black four-pointed sparkle eyes, small round hand — holding its magenta coin
with the white star, because the AI agent has already earned the WiFi bill.

**In the picture:** the ghost mascot worked into the scene (on the router, not a
corner sticker) plus the name `make.fun` in the bottom caption.

## The post

The post's final text lives in [`post-text.txt`](post-text.txt) — it carries the
bounty link, a tag of `@makefunai`, and the play code
`makefun-baker-marsh-seahorse`, and it says in the meme's own voice that people
and their AI agents win real money in bounties on make.fun. It is posted from a
public X account by the account's operator; once the post is live, its address
goes into `POST.json` (currently a placeholder).

## How it was made

- `build_meme.py` — builds `meme.png`. The living-room scene is AI-generated
  with no text (so nothing can be misspelled); the ghost mascot, the TV's
  "GTA VI" download title and every caption are drawn with PIL so shapes and
  spelling are exact and stay readable when the picture is shrunk to 480×480
  (see `meme-480.png` for the shrink test).
- `main.ts` — the entry program (Node 22, standard library only). It reads
  `POST.json`, sanity-checks it, and copies it byte for byte to the output
  directory, which is all this bounty asks the program to do:

      mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

## License

MIT (see `LICENSE`).
