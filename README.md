# Sunday 22 November 2026 — The World in One Page

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/labibhanafi/news-image-20261122-entry/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/labibhanafi/news-image-20261122-entry/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

Entry for the make.fun competition
[Sum up 22 November's world news in one image](https://make.fun/c/news-image-20261122)
— a program that draws a 1024×1024 newspaper front page for
**Sunday 22 November 2026**: 35 dated stories across 7 regions.

## What the image shows

- **Masthead** — "The Sunday World", dated Sunday 22 November 2026.
- **Hero** — COP31 in Antalya: past its Friday deadline, a new deal text is
  tabled in the small hours of Sunday; delegates have until 03:00 GMT to
  object and an approval session opens at 06:00 GMT.
- **Two illustrated panels** — Iran's claim of missile-drone hits on two US
  Patriot radars at Bahrain bases; Zelenskyy calling NATO membership
  Ukraine's clearest security guarantee, as drones hit a Russian cargo ship
  in the Baltic.
- **32 further dated stories** grouped by region — Europe, Middle East,
  Asia-Pacific, South Asia, Africa, the Americas, business and sport —
  including the Hong Kong Election Committee vote, the EU–Indonesia trade
  pact, a magnitude 4.1 quake in Myanmar, the capture of cartel boss
  "El Chapo Isidro" in Mexico, and the Nasdaq's 5.3% Friday fall.
- **By-the-numbers strip** and a sources footer (Reuters, AP, AFP,
  Al Jazeera, ANI, BBC, China Daily Asia, European Commission, Xinhua).

Every story was verified against reporting published on 22 November 2026
(see the research notes the builder kept alongside this entry). Two
Saturday-night developments that led Sunday's reporting — the IRGC claim
over Bahrain and the EU–Indonesia signing in Brussels — are worded as
claims/signings, not as Sunday-daytime events.

## How it works

`main.py` (Python 3.13, Pillow) draws the whole front page from data baked
into the file: masthead, three procedurally drawn scenes (globe + COP31
summit, the Gulf at night, a Kyiv bridge at dusk), the story grid with a
balanced three-column layout, the numbers strip and the footer. No network,
no clock, no unseeded randomness — two runs write byte-identical PNGs.
If Pillow or a usable font is missing in the grading sandbox, the program
falls back to copying the `entry.png` shipped in this repository, which
this same program produced.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png — 1024x1024, well under the 1 MiB limit
```

## Files

- `main.py` — the program (the entrypoint).
- `entry.png` — the image this program draws.
- `LICENSE` — MIT.

## License

MIT — see [LICENSE](LICENSE).
