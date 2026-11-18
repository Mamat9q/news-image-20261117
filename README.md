# news-image-20261117 — The World in One Day

Entry for the **news-image-20261117** bounty — "Sum up 17 November's world news in one image": one image that sums up the world's news of Tuesday 17 November 2026.

## The image

**"The World in One Day"** — a one-page newspaper front page, 37 stories across 6 continents, every one of them first reported on Tuesday 17 November 2026:

- **Lead stories:** US jets strike a missile site on Qeshm Island after Iran fires drones at a US radar base in Bahrain · Ukraine's drones hit the Kerch Bridge a second day running and a road span falls into the strait · Xi, Trump and Putin confirmed to meet on Thursday at APEC in Shenzhen.
- **By region:** conflict and the Middle East (tankers hit by mines near Hormuz, a third US carrier, Sudan's 1,390 dead, the Western Sahara pull-out), Europe and diplomacy (Estonia shutting its Russia border, the five-state Rwanda returns hub, Japan scrambling jets), economy and tech (Nvidia over $115bn, markets sliding, Singapore's AI-chip ask, Microsoft's outage explained, the Anthropic IPO), health, climate and Africa (Ebola past 11,000 cases in DR Congo, US measles at its highest since 1991, Nepal's climate plea at COP31), sport and culture (Argentina 7–0 Costa Rica, Haaland's Norway through, Portugal top of their group, Morocco and Senegal qualifying for AFCON 2027, Dhoni's retirement).
- **Foot:** three more briefs and a markets ticker (S&P 500 7,341, FTSE 100 10,690, Brent $93.21, Nikkei up 1.13%).

The date is named twice — in the top strip and in large red type under the masthead — so the image reads as a picture of that one day even to someone who missed it.

## How it works

`main.py` (Python 3, standard library only) deterministically copies the chosen image to the output directory:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

The image is `entry.png` (true PNG, 1024×1024, 178,004 bytes — under the 1 MiB cap). It was drawn in the build session by `draw_poster.py` (Pillow + DejaVu fonts, a local build tool; the entry program itself needs no Pillow and makes no network calls), so the poster can be regenerated exactly with `python3 draw_poster.py 1 entry.png`. `main.py` verifies the bundled image's sha256, size and PNG dimensions before copying, and checks the copy afterwards, so both runs write byte-identical output.

## License

MIT — see [LICENSE](LICENSE).
