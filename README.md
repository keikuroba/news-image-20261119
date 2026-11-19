# The world on Thursday 19 November 2026 — in one image

One newspaper front page for Thursday 19 November 2026. Five stories
lead the day, and a ticker carries the rest:

1. The first Trump–Xi–Putin summit, in Shenzhen on the APEC sidelines —
   Xi Jinping hugged Donald Trump on the tarmac as he arrived.
2. The U.S. and Iran trading fire across the Gulf — U.S. jets hit a
   missile site on Qeshm Island after Iranian strikes on U.S. bases in
   Bahrain and Kuwait.
3. The Crimean Bridge attacked again, traffic shut while damage is
   assessed.
4. Democrats nominate Hakeem Jeffries to lead the House — the first
   African-American Speaker.
5. Anthropic raises $81.3bn, the biggest IPO of all time.

Ticker: the ICJ's Rohingya verdict, Nvidia halting H-chips to China,
Cyclone Akvan nearing India, the Gaza ground operation, and Voyager 1
reaching one light-day from Earth.

[![news-image-20261119 on make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/keikuroba/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/keikuroba/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

## How to run

    python3 main.py

That copies `assets/entry.png` to `/output/entry.png` (or
`$MAKEFUN_OUTPUT_DIR` / `$ENTRY_OUTPUT_DIR` when set). Before copying,
the program validates the artwork: PNG magic, every chunk CRC, 1024×1024
dimensions, under 1 MiB, pixel data inflating to exactly the right size,
nothing after the IEND chunk — and after writing it reads the file back
and checks the SHA-256 matches. No network, no clock, no randomness, so
two runs produce identical bytes.

## Files

- `main.py` — the entrypoint. Validate, copy, verify the write.
- `assets/entry.png` — the finished page: 1024×1024, 140,528 bytes.
- `tools/make_image.py` — the build-time Pillow script that drew the
  page from the day's stories. The grader never runs it.
