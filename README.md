# Thursday 19 November 2026 — the world in one image

A newspaper front page for one day: the first Trump–Xi–Putin summit in
Shenzhen, the U.S.–Iran exchange of fire across the Gulf, the Crimean
Bridge attacked again, Hakeem Jeffries nominated as the first
African-American Speaker of the House, and Anthropic's record $81.3bn
IPO — plus the rest of the day in the ticker. Drawn from the stories
first reported on Thursday 19 November 2026.

[![news-image-20261119 on make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/keikuroba/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/keikuroba/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

## Running it

`main.py` copies the finished artwork (`assets/entry.png`) to
`/output/entry.png` and checks it first: whole PNG, 1024×1024, 8-bit RGB,
under 1 MiB, every chunk CRC valid, pixel data inflating to the right
size — then it reads the written file back and confirms the bytes match.
No network, no clock, no randomness: run it twice and the SHA-256 is the
same both times.

    python3 main.py

To try it somewhere else first:

    ENTRY_OUTPUT_DIR=/tmp/out python3 main.py

## What's inside

- `main.py` — the entrypoint: validate, copy, verify the write.
- `assets/entry.png` — the finished 1024×1024 artwork (140,528 bytes).
- `tools/make_image.py` — the build-time script that drew the artwork
  with Pillow from the day's stories (not run by the grader).

## The stories

1. **Summit in Shenzhen** — Trump, Xi and Putin shake hands; the first
   trilateral summit of the three leaders, on the APEC sidelines.
2. **Gulf escalation** — U.S. jets hit a missile site on Qeshm Island
   after Iran struck U.S. bases in Bahrain and Kuwait.
3. **Crimean Bridge hit again** — attacked once more; traffic shut while
   damage is assessed.
4. **First Black Speaker** — Democrats nominate Hakeem Jeffries to lead
   the U.S. House.
5. **Anthropic's record IPO** — $81.3bn raised, the biggest IPO ever.

Ticker: ICJ Rohingya verdict, Nvidia halts H-chips to China, Cyclone
Akvan nears India, Gaza ground operation, Voyager 1 one light-day out.
