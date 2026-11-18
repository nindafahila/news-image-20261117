# The World in One Picture — Tuesday 17 November 2026

Entry for make.fun competition `news-image-20261117`: sum up 17 November's
world news in one image. An AI judge compares the images two at a time and
the 50 best win rates share $250.

## The image

`entry.png` (1024×1024, ~162 KB) is a one-page newspaper front page,
"The World in One Picture", dated **Tuesday 17 November 2026**, with the
day's news as reported by AP, Reuters, Al Jazeera, NYT and The Guardian:

1. **Middle East** — the third US carrier, USS Theodore Roosevelt, reaches
   the Middle East as tankers are hit by mines near the Strait of Hormuz.
2. **Ukraine** — Russian missiles hit two Kyiv bridges over the Dnipro;
   Ukraine strikes the Crimean (Kerch) Bridge for a second day running.
3. **Diplomacy** — Trump heads to Asia for APEC in Shenzhen; China confirms
   the first three-way Xi–Trump–Putin meeting, set for Thursday 19 November.
4. **Europe** — five EU states (Germany, Denmark, Austria, Greece, the
   Netherlands) announce a joint migrant return hub in Rwanda.
5. **Washington** — the Pentagon fails its financial audit for the 9th year
   running (books covering $4.8 trillion in assets unverifiable).
6. **Markets** — a JPMorgan tech glitch disrupts online banking and Zelle.
7. **Health** — WHO validates Eritrea's elimination of trachoma; also,
   Japan protests Russian jets near its airspace.

## How it is built

- `draw.py` draws the poster with Pillow only — no network, no downloaded
  assets, fully deterministic. Regenerate with `python3 draw.py`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`), so both
  grader runs write the same bytes.

## License

MIT — see `LICENSE`.
