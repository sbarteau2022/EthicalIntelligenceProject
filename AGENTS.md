# The Ethical Intelligence Project — Agent Instructions

## Project Overview

The public site for The Ethical Intelligence Project, powered by Elle AI. It began as the AstroWind template; the template's blog, demo pages and widget library have since been removed and the public surfaces rebuilt on the project's own **dark "Observer" design system**.

**Stack:** Astro v6 | TypeScript 5.9 | three.js | Sharp
Tailwind is still installed and loaded by `Layout.astro`, but the overhauled pages do not use utility classes — they use the design system in `src/assets/styles/eip.css`.

## The design system (read this before touching a page)

`src/assets/styles/eip.css` is the single stylesheet for every public surface. Everything is scoped under `.eip`. Tokens: void `#06060a`, base `#0b0b11`, raised `#101018`, gold `#c9a84c` / `#e8cc88`, ivory `#f5f0e8`, text `#eee8d8` / `#9a9480` / `#5a5448`. Type: Cormorant Garamond (display), Instrument Sans (UI), DM Mono (data).

Three scopes exist, and the distinction matters:

| Scope          | Used by                                           | Why                                                                                                                               |
| -------------- | ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `.eip`         | every rebuilt marketing page, via `EipPage.astro` | the normal case                                                                                                                   |
| `.eip.eih`     | the nine Atlas pages                              | they still need hub.css for their stages; `eip.css` is imported **second** so its surface tokens win                              |
| `.eip.eip-app` | `/optimus`, `/engine`                             | their scripts build DOM with inline `var(--t1)` etc. from hub.css's vocabulary, so `eip.css` shadows those names with dark values |

`src/eip.ts` is the content model (products, engines, principles, corpus list, facts, socials, footer columns). Edit lists there, not in pages, or the nav and pages will drift.

## Things that must not be broken

- **The Atlas master renderings** (`/master-atlas` plus atlas, neural, staircase, hologram, fracture, orbital, entropy, cmb) and the eight `src/data/*-snapshot.json` files. Positions are read verbatim from the snapshots; the renderers re-derive nothing. Only their nav/footer has been swapped — leave the renderer code alone.
- **The hero globe** (`src/components/eip/HeroGlobe.astro`). Its look is the product of a long design iteration. The comment block at the top records what was deliberately **cut** (comet, weather, equator line, every directional light, the circular frame) — do not "improve" those back in.
  Note the module invokes `start()` at the **bottom** on purpose: `start` is hoisted but the `const`s it reaches are not, so calling it earlier throws a TDZ error and the globe silently never draws.
- **Live wiring.** `window.EIH` (from `HubAuth.astro`) owns Google OAuth and authenticated worker calls; an element with `id="eih-acct"` is auto-wired as the sign-in/out toggle. Real endpoints in use: `/api/elle-oauth`, `/api/elle-conversation`, `/api/widget-chat`, `/api/contact`, `/api/optimus-journal`, `/api/corpus-papers|corpus-paper|corpus-series`.
- **Standing copy corrections.** The Observer is an **independent research initiative, not a 501(c)(3)** — the only permitted mention is the explicit "not yet a 501(c)(3)". No page may reference **Hermann, Missouri**.

## Coastline data

`public/data/land-50m.json` is the public-domain Natural Earth topology the globe rasterises into its texture. It is vendored deliberately rather than fetched from a CDN so the render can never silently fall back to the coarse offline outlines. Keep it in `public/`.

## Quick Reference

| Command           | Purpose                             |
| ----------------- | ----------------------------------- |
| `npm run dev`     | Start dev server at localhost:4321  |
| `npm run build`   | Production build to `./dist/`       |
| `npm run preview` | Preview production build locally    |
| `npm run check`   | Run astro check + ESLint + Prettier |
| `npm run fix`     | Auto-fix ESLint + Prettier issues   |

**Node.js requirement:** >= 22.12.0

## Architecture

### Directory Structure

```
src/
  assets/styles/
    eip.css            # THE design system — dark Observer, all public surfaces
    hub.css            # older light system; still powers the Atlas stages
    tailwind.css       # Tailwind v4 config (loaded by Layout, largely unused now)
  components/
    eip/               # EipPage, EipNav, EipFooter, HeroGlobe  ← the new shell
    hub/               # HubAuth (live OAuth), HubNav/HubFooter (legacy), AtlasGraph
    common/            # Image, Metadata, Analytics, ToggleTheme
    CustomStyles.astro # CSS variables for colors and fonts
  data/
    corpus.ts          # the volume→paper tree behind /core-works
    learn.ts           # the Atlas Edu curriculum (shared by /learn)
    *-snapshot.json    # Atlas rendering source data — DO NOT EDIT
  eip.ts               # content model: products, engines, principles, facts…
  hub.ts               # WORKER_URL + legacy hub tabs/socials
  layouts/             # Layout.astro, MarkdownLayout.astro
  pages/               # file-based routing
  utils/               # images.ts, permalinks.ts, frontmatter.ts, directories.ts
  config.yaml          # site configuration (loaded as virtual module)
  types.d.ts           # TypeScript type definitions
public/data/land-50m.json  # Natural Earth coastlines for the hero globe
vendor/integration/        # custom Astro integration for config loading
design-handoff/            # the Claude Design bundle this overhaul was built from
```

### Adding a page

```astro
---
import EipPage from '~/components/eip/EipPage.astro';
const metadata = { title: '…', description: '…' };
---

<EipPage {metadata} current="/your-route">
  <section><div class="shell sec-y">…</div></section>
</EipPage>
```

`EipPage` supplies the scope, the nav, the footer and the auth modal. Compose with the system's classes (`shell`, `sec-y`, `on-base`, `kicker`, `lede`, `prose`, `split`, `facts`, `tiles`, `btn btn-gold` / `btn-ghost`, `chip`) rather than new one-off CSS.

### Path Aliases

Use `~/` to import from `src/`:

```typescript
import Image from '~/components/common/Image.astro';
import { SITE } from 'astrowind:config';
```

### Configuration System

Site config lives in `src/config.yaml` and is loaded as a Vite virtual module `astrowind:config` by the custom integration in `vendor/integration/`. Exports: `SITE`, `I18N`, `METADATA`, `APP_BLOG`, `UI`, `ANALYTICS`. `APP_BLOG` is vestigial — the blog was removed — but the integration's schema still expects the key, so leave it in place.

## Tailwind CSS v4

Still installed and imported by `Layout.astro`, so its preflight applies, but the rebuilt pages use `eip.css` instead of utility classes. Configuration is CSS-first in `src/assets/styles/tailwind.css`; the Vite plugin `@tailwindcss/vite` is configured in `astro.config.ts` (not as an Astro integration). Colour/font variables live in `src/components/CustomStyles.astro`.

Note `Layout.astro` puts `bg-page` on `<body>`; `eip.css` overrides it via `html:has(.eip) body`.

## Component Patterns

- Props extend interfaces from `~/types`
- Use `class:list` for conditional classes
- Use named slots for layout composition
- Prefer a shared class in `eip.css` over a per-page `<style>` block
- Page-level scripts are `is:inline` and pass server values with `define:vars`

## Image Handling

`src/components/common/Image.astro` supports:

- Local images via `astro:assets` (optimized by Sharp)
- Remote images via Unpic CDN
- Allowed domains (for providers Unpic can't detect, processed by Sharp): `cdn.pixabay.com`

Hero images use `loading="eager"` and `fetchpriority="high"`.

## Verification Checklist

After changes, always verify:

1. `npm run build` succeeds
2. `npm run check` passes (astro check + ESLint + Prettier)
3. Visual check in a browser at **1440 and 390**: the homepage (the globe must actually draw — check the canvas is sized to the viewport, not 300×150), `/master-atlas`, and any page you touched
4. No horizontal page scroll at 390px — the nav pill and the hero canvas are the two things that have caused it

## House format for papers and submissions (standing instruction)

All papers, preprints, and submission packages use the **Corpus Forge
house format** — jacket page, colophon with SHA-256 source fingerprint,
Pagella/Poppins/Liberation Mono typography. The spec and the generator
live in `docs/preprints/HOUSE_FORMAT.md` and `docs/preprints/corpus_forge.py`;
add a config dict per paper and run the generator rather than hand-building
PDFs. Reference artifact: the Noema submission of "Formed Before It Became"
(July 2026).
