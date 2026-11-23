# The Day in the World — Monday 23 November 2026

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Kegelapan-ai/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Kegelapan-ai/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Built for the make.fun bounty: https://make.fun/bounty/news-image-20261123

An entry for the [make.fun bounty “Sum up 23 November's world news in one
image”](https://make.fun/bounty/news-image-20261123): one picture that sums
up Monday 23 November 2026, drawn as a one-page newspaper front page. The
date is printed large at the top, so the picture stands on its own — a
viewer who missed the day can tell what happened from the image alone.

## The six stories

Every claim in the picture was checked against live reporting published on
23 November 2026. Where a claim is one side's statement, the picture says
so (“Ukraine says…”, “Iran said…”).

1. **NATO meets after missiles land in Poland (lead story).** NATO
   ambassadors meet in Brussels on Monday after three Russian Kh-101
   cruise missiles flew into Polish airspace on Friday and crashed in the
   south-east. Polish prosecutors said on Sunday that all three were
   Kh-101s, made in the fourth quarter of 2026 at Dubna. NATO chief Mark
   Rutte said the alliance will defend “every inch” of Polish territory.
   Sources: Reuters.
2. **Ukraine says sea drones sank a Russian warship off Libya.**
   President Zelenskyy said on Monday that seven Ukrainian naval drones
   sank the Russian corvette Merkury off Libya. The cargo ship MV Angara
   was also hit. Source: Reuters.
3. **Dymer toll rises to 11 after drone hits flats.** The death toll rose
   to 11 on Monday after rescuers pulled another body from a block of
   flats in Dymer, near Kyiv, hit by a Russian drone on Sunday. Nine
   people were rescued. Source: Reuters.
4. **Factory fire kills 24; about 30 still missing (Indonesia).**
   Indonesia confirmed on Monday that 24 people died in a fire that tore
   through a candy factory in Cikande, Banten, on Saturday evening.
   Rescuers were still searching the burned-out building. Source: Reuters.
5. **Iran vows to fight US blockade “with all tools”.** Iran said on
   Monday it will use all available means to confront the US naval
   blockade of its ports. President Trump had said on Sunday that US
   forces would sink ships trying to break it. Sources: Reuters (via
   reporting of the Foreign Ministry briefing and the Fox News interview).
6. **“Trump Route” breaks ground in Armenia.** Armenia launched the
   US-backed Trump Route for International Peace and Prosperity (TRIPP) on
   Monday, linking mainland Azerbaijan with its Nakhchivan exclave through
   Armenian territory. Sources: RIA Novosti, Anadolu (via World Brief Now).

Also in the footer strip (all weekend stories, dated as such): Democrats
won at least 258 House seats on Sunday, their biggest majority since 1992
(AP, Reuters); more than 1,600 Delta flights were delayed on Sunday after
a weight-and-balance system failure (Wall Street Journal, FlightAware);
the COP31 summit in Türkiye ended on Sunday with no deal — the longest
climate talks ever (UN News, AP); Israeli forces hit a truck in Gaza on
Saturday and three people were killed, Gaza's Health Ministry said
(Just Security / Reuters).

## Deliberately left out

- **Stories from earlier days with no new 23 November development.** The
  Danish accusation that Russia plotted to kill rapper Kyivstoner (20
  November), the Common Cents Act ending penny production (signed Friday
  20 November), and the capture of cartel boss “El Chapo Isidro” (21
  November) all belong to earlier days, so none of them leads the page.
- **Unverified claims.** Iran's claim that a supertanker sank after
  hitting a mine near the Strait of Hormuz is reported by Iranian sources
  only and could not be confirmed from independent reporting, so it is not
  in the picture. The Merkury sinking is phrased as Ukraine's claim, as
  reported by Reuters. No casualty figure is used where the sources
  conflicted — the Indonesian factory toll uses the figure confirmed by
  the presidential adviser on Monday (24 dead, about 30 missing).

## How it is made

`build_image.py` draws the front page with Pillow only: DejaVu fonts from
the system, fixed colours and positions, no clock, no randomness, no
network. It writes `image.png` (1024×1024, about 140 KB). `main.py` is the
competition entry point (Python standard library only): it copies
`image.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, defaulting to
`/output/entry.png`.

## Build and run

```sh
python3 build_image.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Two runs of `main.py` write byte-identical files (same SHA-256 as
`image.png`), and re-running `build_image.py` reproduces `image.png`
exactly. The image was viewed and checked for legibility, overlaps and
clipping before this was finished.

## License

MIT — see `LICENSE`.
