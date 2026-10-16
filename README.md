# The Ethical Intelligence Project

**Powered by Elle AI**

Community-based intelligence infrastructure that transforms complexity into action. The Ethical Intelligence Project builds transparent, auditable, non-extractive tools that help working people navigate the systems written for specialists — government programs, healthcare, legal processes, grants, and civic institutions.

> The information exists. The resources exist. The opportunities exist. For millions of working people, the problem is access. We exist to close that gap.

This repository contains the project's public website — a statically generated [Astro](https://astro.build/) site (built on the AstroWind template) carrying the dark "Observer" editorial tone, with Elle, our corpus-grounded intelligence, woven throughout.

- 🔗 **Production:** [ethicalintelligenceproject.pages.dev](https://ethicalintelligenceproject.pages.dev)
- 💬 **Talk to Elle:** [/elle](https://ethicalintelligenceproject.pages.dev/elle)
- 🧭 **The Atlas:** [/master-atlas](https://ethicalintelligenceproject.pages.dev/master-atlas) — nine math-driven 3D renderings with committed generators and a claims ledger; the complete record lives in [`docs/ATLAS.md`](./docs/ATLAS.md)

For agent/AI-assistant conventions (house format, verification checklist, path aliases, etc.), see [AGENTS.md](./AGENTS.md).

## Atoma Engineering — staged design

The `staging/atoma-engineering` branch adds the reviewed eggshell/blue/titanium
marketing design at `/engineering`, with a printable brand book at
`/engineering/brand`. The existing homepage, Observer/Atlas pages, renderers,
OAuth, and live integrations are unchanged. This is an additive design preview,
not a production homepage replacement.

The kit includes separate Atoma and Grant Intelligence identities, SVG/PNG
artwork, social cards, self-hosted fonts/licenses, CSS/JSON tokens, and source.
Download `/assets/brand/atoma-brand-package.zip`. The product links open Grant
Intelligence's independent Worker host, not this site's unrelated `/app`.
Contact remains the labeled placeholder `hello@atoma.example`; project briefs
stay in page memory and can be copied/downloaded without submission or storage.

Build the kit with `npm run brand:build` (Node.js, uv, zip, and installed Sharp).
Build/preview the site with `npm run build` and
`npm run preview -- --host 127.0.0.1 --port 8794`, then run
`npm run test:brand -- --url http://127.0.0.1:8794 --site-regressions`.
Add `--artifacts /absolute/output/directory` for review captures.
See [the design specification](./docs/ATOMA_DESIGN_PACKAGE.md) and
[standalone kit instructions](./docs/ATOMA_PACKAGE_README.md).

Only pushes to `main` trigger the production deploy workflow. This staging
branch is not merged; a PR may trigger the repository's preview workflow.
Unrelated local preprint deletions and private agent settings are excluded.

<br>

## Table of Contents

- [What's inside](#whats-inside)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
  - [Requirements](#requirements)
  - [Environment variables](#environment-variables)
  - [Commands](#commands)
- [Project structure](#project-structure)
- [Configuration](#configuration)
- [Elle integration](#elle-integration)
- [The Atlas](#the-atlas)
- [Docs & corpus](#docs--corpus)
- [CI/CD & Deploy](#cicd--deploy)
- [Acknowledgements](#acknowledgements)
- [License](#license)

<br>

## What's inside

The site presents the project as one presence with nine expressions — the **Nine Engines**:

| #   | Engine                    | Focus                                | Where it lives                                                                                                                |
| :-- | :------------------------ | :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| 01  | Elle Law                  | Rights & legal reasoning             | external — [elle-law.pages.dev](https://elle-law.pages.dev)                                                                   |
| 02  | Harmonizer                | Mental health & peer support         | external — [harmonizer-two.vercel.app](https://harmonizer-two.vercel.app)                                                     |
| 03  | Atlas Edu                 | Education & navigation               | `/learn` (in this repo)                                                                                                       |
| 04  | Agricultural Intelligence | USDA & farm resources                | `/business` (in this repo)                                                                                                    |
| 05  | Healthcare Navigation     | Benefits & patient rights            | `/elle` (in this repo)                                                                                                        |
| 06  | Small Business Hub        | Licensing, grants & compliance       | `/business` (in this repo)                                                                                                    |
| 07  | Civic Intelligence        | Government documents, translated     | `/elle` (in this repo)                                                                                                        |
| 08  | RAPID²AI                  | Hospitality operational intelligence | external — [rapidai.pages.dev](https://rapidai.pages.dev/coo/), plus operator surfaces in this repo (`/app`, `/chef`, `/coo`) |
| 09  | The Observer              | Research & testimony                 | `/observer` (in this repo)                                                                                                    |

(See the `engines` array in [`src/pages/index.astro`](./src/pages/index.astro) for the source of this table.)

Beyond the engines, the site includes:

- **The Hub** — `/optimus` (append-only journal + manuscript reader), `/engine` (the structural analysis engine, backed by `/api/falcon`), `/business` (Small Business Hub), `/observer`, and `/learn` (Atlas Edu's course module). These share `src/components/hub/` (`HubNav`, `HubFooter`, `HubAuth`) and `src/assets/styles/hub.css`.
- **`/elle`** — the full Elle chat experience (corpus-grounded answers; sign-in unlocks persistent memory).
- **`/glass`** — the MadMind Institute corpus landing page (a 501(c)(3) initiative of the project).
- **`/principled`** — "Principled Intelligence," the flagship page explaining the whole system end to end.
- **`/app`, `/chef`, `/coo`** — RAPID²AI's Google-OAuth-gated operator surfaces (chat intelligence, chef view, COO dashboard), talking to the `elle-worker` Cloudflare Worker's `/api/atlas` door.
- **The Atlas suite** — nine pages of math-driven 3D renderings (`/atlas`, `/neural-atlas`, `/master-atlas`, `/orbital-atlas`, `/staircase-atlas`, `/fracture-atlas`, `/hologram-atlas`, `/cmb-atlas`, `/entropy-atlas`). See [The Atlas](#the-atlas) below.
- **`/design-system`** — the "Civic Luminance" design system reference (not indexed by search).
- Standard marketing/legal pages: `/about`, `/services`, `/pricing`, `/contact`, `/terms`, `/privacy`, and a blog under `/[...blog]`.

Alongside these pages, the site surfaces the **corpus** (the intellectual framework Elle reasons from — see [Docs & corpus](#docs--corpus)), the project's **AI principles** (transparent, auditable, human-centered, non-extractive, community-governed), and ways to get involved.

<br>

## Tech stack

- **[Astro v6](https://astro.build/)** — static site generation
- **[Tailwind CSS v4](https://tailwindcss.com/)** — CSS-first styling
- **TypeScript** · **MDX** · **Sharp** (image optimization) · **astro-icon** (Tabler + Flat Color icons)
- **[Three.js](https://threejs.org/)** — the 3D renderings powering the Atlas suite
- **Elle** — corpus-grounded intelligence served via a separate Cloudflare Worker (`elle-worker`), called over HTTPS from this static site
- **Google Identity Services** — OAuth sign-in for `/elle`, the Hub, and the RAPID²AI operator surfaces

<br>

## Getting started

### Requirements

- **Node.js >= 22.12.0**

Install dependencies:

```shell
npm install
```

### Environment variables

The build reads these at build time (all optional — the site degrades gracefully without them):

| Variable                      | Used for                                                                                                                                                                                                                                                                                                                                                            |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `PUBLIC_GOOGLE_CLIENT_ID`     | Google OAuth "Web application" client ID, baked into the static build so sign-in on `/elle`, the Hub (`HubAuth`), and RAPID²AI surfaces render a working button. Left unset → sign-in shows a "temporarily unavailable" message instead of a broken button. The matching `elle-worker` secret (`GOOGLE_CLIENT_ID`, same value) must also be set on the worker side. |
| `PUBLIC_RAPIDAI_CHAT_API_URL` | Overrides the RAPID²AI chat endpoint (`/app`); defaults to `https://elle-worker.sbarteau2022.workers.dev/api/atlas`.                                                                                                                                                                                                                                                |

### Commands

All commands are run from the root of the project, from a terminal:

| Command             | Action                                             |
| :------------------ | :------------------------------------------------- |
| `npm install`       | Installs dependencies                              |
| `npm run dev`       | Starts local dev server at `localhost:4321`        |
| `npm run build`     | Build your production site to `./dist/`            |
| `npm run preview`   | Preview your build locally, before deploying       |
| `npm run check`     | Run `astro check` + ESLint + Prettier              |
| `npm run fix`       | Auto-fix ESLint and Prettier issues                |
| `npm run astro ...` | Run CLI commands like `astro add`, `astro preview` |

> **Note:** `npm run check` is what CI (and the deploy workflow) runs. Run `npm run fix` before committing to keep Prettier and ESLint green. There is currently no automated test suite (`npm test` is not defined; CI's build job has a commented-out test step).

<br>

## Project structure

```
/
├── public/                          # decapcms config, media assets
├── src/
│   ├── assets/styles/tailwind.css   # Tailwind v4 theme tokens & utilities
│   ├── assets/styles/hub.css        # Shared styles for the Hub pages
│   ├── components/
│   │   ├── common/                  # Image, Metadata, Analytics, ToggleTheme
│   │   ├── ui/                      # Button, Headline, WidgetWrapper, ItemGrid
│   │   ├── widgets/                 # Hero, Features, Pricing, Header, Footer
│   │   ├── hub/                     # HubNav, HubFooter, HubAuth, AtlasGraph
│   │   ├── blog/                    # SinglePost, List, Pagination, Tags
│   │   └── CustomStyles.astro       # CSS variables for colors and fonts
│   ├── content.config.ts            # Content Collections schema
│   ├── data/post/                   # Blog posts (.md, .mdx)
│   ├── data/*.json                  # Committed Atlas snapshots (generator output)
│   ├── layouts/                     # Layout, PageLayout, MarkdownLayout
│   ├── pages/                       # File-based routing
│   │   ├── index.astro              # Homepage (Observer tone, Nine Engines)
│   │   ├── elle.astro               # Talk to Elle — chat experience
│   │   ├── optimus.astro, engine.astro, business.astro, observer.astro, learn.astro  # The Hub
│   │   ├── glass.astro, principled.astro, edu.astro   # Corpus/marketing landings
│   │   ├── atlas.astro, neural-atlas.astro, master-atlas.astro,
│   │   │   orbital-atlas.astro, staircase-atlas.astro, fracture-atlas.astro,
│   │   │   hologram-atlas.astro, cmb-atlas.astro, entropy-atlas.astro  # The Atlas suite
│   │   ├── app/, chef/, coo/        # RAPID²AI operator surfaces (Google-OAuth-gated)
│   │   └── ...                      # about, services, pricing, contact, blog, landing
│   ├── config.yaml                  # Site configuration (virtual module)
│   ├── navigation.ts                # Header & footer navigation
│   └── utils/                       # blog.ts, images.ts, permalinks.ts, frontmatter.ts
├── scripts/                          # Python/Node generators for Atlas snapshots
├── docs/                             # Corpus: essays, preprints, writing, ATLAS.md (see below)
├── vendor/integration/               # Custom Astro integration that loads src/config.yaml
├── .agents/skills/                   # How-to notes for adding pages/components/blog posts
├── astro.config.ts
└── package.json
```

Astro looks for `.astro` or `.md` files in `src/pages/`; each file becomes a route based on its name. Static assets that need no transformation live in `public/`; assets imported directly live in `src/assets/`.

<br>

## Configuration

Site-wide configuration lives in `src/config.yaml` (loaded as the virtual module `astrowind:config` by the integration in `vendor/`). The branding, SEO metadata, and analytics are set there:

```yaml
site:
  name: The Ethical Intelligence Project
  site: 'https://ethicalintelligenceproject.pages.dev'

metadata:
  title:
    default: The Ethical Intelligence Project — Powered by Elle AI
    template: '%s — The Ethical Intelligence Project'
```

To customize the look:

- `src/components/CustomStyles.astro` — CSS variables for colors and fonts
- `src/assets/styles/tailwind.css` — Tailwind theme tokens (`@theme`), custom utilities (`@utility`), and plugins
- `design-tokens.json` — the underlying design-token source (colors, typography) that the tokens above are derived from
- `src/pages/index.astro` — the homepage's self-contained dark "Observer" styles (scoped under `#tep`)

<br>

## Elle integration

Elle is served by an external Cloudflare Worker (`elle-worker`, a separate repository). The homepage loads a floating chat widget, and `/elle` is the full conversation experience:

- **Widget:** `https://elle-worker.sbarteau2022.workers.dev/widget.js`
- **Chat / auth endpoints:** `/api/widget-chat`, `/api/elle-conversation`, `/api/elle-auth`, `/api/elle-oauth`
- **RAPID²AI door:** `/api/atlas`, used by the operator surfaces under `/app`, `/chef`, `/coo`
- **Structural Analysis Engine:** `/api/falcon`, used by `/engine`

Guests get corpus-aware answers; signed-in users (Google OAuth) get full corpus reasoning and persistent memory (the Optimus journal).

<br>

## The Atlas

`/master-atlas` and its companion pages are nine math-driven 3D renderings — a unified function, a knowledge structure, and seven "anchor" pages where a real physical/mathematical result (Kirkwood gaps, the devil's staircase, off-axis holography, the CMB spectrum, entropy production, etc.) is computed by a committed generator and then rendered verbatim, with a claims ledger tracking what's demonstrated vs. proposed.

Each page has a corresponding generator under `scripts/` and a committed JSON snapshot under `src/data/`:

| Page               | Generator                                | Snapshot                                  |
| ------------------ | ---------------------------------------- | ----------------------------------------- |
| `/atlas`           | `scripts/generate-harmonic-snapshot.mjs` | `src/data/harmonic-snapshot.json`         |
| `/neural-atlas`    | `scripts/generate-neural-snapshot.py`    | `src/data/neural-structure-snapshot.json` |
| `/master-atlas`    | (reads both snapshots above)             | —                                         |
| `/orbital-atlas`   | `scripts/generate-orbital-snapshot.py`   | `src/data/orbital-snapshot.json`          |
| `/hologram-atlas`  | `scripts/generate-hologram-snapshot.py`  | `src/data/hologram-snapshot.json`         |
| `/staircase-atlas` | `scripts/generate-circlemap-snapshot.py` | `src/data/circlemap-snapshot.json`        |
| `/fracture-atlas`  | `scripts/generate-fracture-snapshot.py`  | `src/data/fracture-snapshot.json`         |
| `/cmb-atlas`       | `scripts/generate-cmb-snapshot.py`       | `src/data/cmb-snapshot.json`              |
| `/entropy-atlas`   | `scripts/generate-entropy-snapshot.py`   | `src/data/entropy-snapshot.json`          |

The Node generator needs no extra dependencies; the Python generators require `numpy` (`pip install numpy`) and take from a few seconds up to several minutes to run. See [`docs/ATLAS.md`](./docs/ATLAS.md) for the full record, the dependency map between pages, and exact regeneration commands.

<br>

## Docs & corpus

`docs/` holds the project's written record, separate from the website code:

- **[`docs/ATLAS.md`](./docs/ATLAS.md)** — the complete Atlas record (see above).
- **`docs/essays/`** — long-form essays (e.g. `FORMED_BEFORE_BECAME_AEON.md`, `SIX_REFUTATIONS_ASTERISK.md`) written alongside the Atlas build.
- **`docs/preprints/`** — papers and submission packages. All use the **Corpus Forge house format** (jacket page, colophon with SHA-256 source fingerprint); the spec is in `HOUSE_FORMAT.md` and the generator is `corpus_forge.py` — add a config dict per paper and run the generator rather than hand-building PDFs. Contains the "Superposition, Holding" preprint (source, generated `.pdf`/`.docx`).
- **`docs/writing/`** — prose written alongside the Atlas build sessions (see `docs/writing/README.md` for the full index), plus `numbers-audit.md`, a self-audit of the Atlas's headline numbers.
- **`docs/DESIGN-ANCHOR.md`, `docs/PUBLISHING_MASTER_PLAN.md`** — internal design and publishing notes.

<br>

## CI/CD & Deploy

Two GitHub Actions workflows run on every PR and push to `main` (`.github/workflows/`):

- **`actions.yaml`** — `build` (installs, `npm run build`) and `check` (`npm run check`: `astro check` + ESLint + Prettier).
- **`deploy.yml`** — builds and deploys to **Cloudflare Pages** (project `ethicalintelligenceproject`) via `wrangler pages deploy`. Pushes to `main` deploy to production; pull requests get a branch-named preview URL; it can also be run manually (`workflow_dispatch`). Requires the `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID` repository secrets — without them the build still runs but the deploy step is skipped with a warning. `PUBLIC_GOOGLE_CLIENT_ID` is an optional secret baked into the build (see [Environment variables](#environment-variables)).

The site builds to static files in `dist/` and can be hosted anywhere. Besides Cloudflare Pages, it's configured for:

- **Netlify** (`netlify.toml`) and **Vercel** (`vercel.json`) — set the build command to `npm run build` and the output directory to `dist`. Avoid calling the `vite`/`astro` binaries directly as the build command — use the `package.json` script so the locally installed CLI is found. `vercel.json` also sets security headers (CSP, HSTS, etc.) and long-lived caching for `/_astro/*`.
- **Docker** (`Dockerfile`, `docker-compose.yml`) — multi-stage build that serves the static output with `nginx` (config in `nginx/nginx.conf`) on port `8080`. Run with `docker compose up`.

```shell
npm run build
```

<br>

## Acknowledgements

Built on the [AstroWind](https://github.com/arthelokyo/astrowind) template, originally created by **Arthelokyo** and maintained by its community of contributors. Elle's corpus is co-authored with Claude (Anthropic).

## License

Licensed under the MIT license — see the [LICENSE](./LICENSE.md) file for details.
