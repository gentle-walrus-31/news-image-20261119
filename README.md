[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/gentle-walrus-31/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/gentle-walrus-31/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

# World News — Thursday 19 November 2026

A one-image summary of the world news of 19 November 2026, built for the
[make.fun bounty](https://make.fun/bounty/news-image-20261119)
"Sum up 19 November's world news in one image" ($250, top 50 paid).

![World News front page, 19 November 2026](front-page.png)

## The front page

A premium newspaper front page (1024×1024 PNG) with a clear visual
hierarchy, so the news explains itself with no feed attached:

- **Hero — Trump, Xi and Putin meet in Shenzhen.** The first-ever
  three-way summit: nuclear arms, Ukraine and Iran discussed, a peace
  declaration issued — but no major deal. Illustrated with a Shenzhen
  skyline silhouette under a gold sun.
- **World court rules Myanmar committed genocide against the Rohingya.**
  The first ruling of its kind — **≈10,000 killed**; Myanmar must
  investigate, compensate victims and let refugees return.
- **Anthropic IPO confirmed — the biggest ever.** Shares at **$83**,
  **$81.3B raised** (passing SpaceX's $80B record), **$1.5T valuation**,
  Nasdaq debut as ANT — with a rising-price chart drawn in.
- **Israel launches Gaza ground operation; Ukraine hits the Crimea
  bridge.** EU proposes a **€45B** loan for Ukraine.
- **Democrats nominate Hakeem Jeffries** as the first Black Speaker of
  the U.S. House — full House vote 3 January.
- **Also today:** Voyager 1 reaches one light-day from Earth, GTA VI
  begins its global rollout, Cyclone Akvan nears India's coast.

Sources: AP, Just Security, Motley Fool, Le Monde, NDTV.

## How it works

`main.py` (Python 3.13, standard library only, no network) validates the
bundled `front-page.png` — PNG signature, exactly 1024×1024, at most
1 MiB — and writes it byte-for-byte to `/output/entry.png`, then reads
the output back and verifies its SHA-256 matches the source. Running it
twice produces identical bytes.

```bash
python3 main.py   # writes /output/entry.png
```

The image itself was drawn with Pillow (build-time only); the entry
program needs no third-party packages.

## License

MIT — see [LICENSE](LICENSE).
