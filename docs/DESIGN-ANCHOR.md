# Design Anchor — the Atlas homepage

The homepage hero is anchored to **GitHub's 2020 globe homepage** ("Where the
world builds software") — the canonical "epic globe" landing page — restyled
in this project's gold-on-black palette (see the Atlas Analytics concept art
in the brand references).

Anchor: <https://github.blog/engineering/engineering-principles/how-we-built-the-github-globe/>
Secondary typography anchor: Linear.app (dark, glow, oversized display type).

## What we take from the anchor

| Anchor move                                                           | How Atlas applies it                                                                 |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| The globe is the stage, not an illustration                           | Atlas fills the hero band; headline sits above it in the same dark space             |
| Activity arcs across the surface                                      | Gold great-circle arcs pulse across the globe — the engines working around the world |
| Atmosphere halo                                                       | Soft gold rim-glow around the globe edge against near-black                          |
| Instant first paint (GitHub crossfades an SVG placeholder into WebGL) | Atlas is pure SVG + CSS from the start — zero JS boot, nothing to crossfade          |
| Interactivity with purpose (hover a PR arc → see it)                  | Five orbit doors are real links: chat, corpus, journal, mission, engines             |
| Massive serif-weight display headline                                 | Cormorant Garamond at clamp(2.2–3.4rem), white on black                              |

## What we deliberately do differently

- **No WebGL.** GitHub needed three.js for live PR data; Atlas's five doors are
  static routes, so SVG keeps it instant, accessible, and dependency-free.
  If live data ever matters (e.g. real corpus-ingest events), the upgrade path
  is `three-globe`, per the anchor's own write-up.
- **Saturn rings.** From the brand concept art, not the anchor — they carry the
  "Atlas" identity.
- **One gold.** GitHub uses blue/pink arcs; we stay monochrome gold on black,
  matching the rest of the hub design system's single-accent rule.

## Palette (the `.atlas-hero` scope in `src/pages/index.astro`)

Space black `#05060a` · card `#0d0f16` · text `#e8e4dc` / `#9ca3af` /
`#6b7280` · gold `#c9902f` · bright gold `#f5b942`.
