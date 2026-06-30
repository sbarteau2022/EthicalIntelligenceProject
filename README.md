# The Ethical Intelligence Project

**Powered by Elle AI**

Community-based intelligence infrastructure that transforms complexity into action. The Ethical Intelligence Project builds transparent, auditable, non-extractive tools that help working people navigate the systems written for specialists — government programs, healthcare, legal processes, grants, and civic institutions.

> The information exists. The resources exist. The opportunities exist. For millions of working people, the problem is access. We exist to close that gap.

This repository contains the project's public website — a statically generated [Astro](https://astro.build/) site (built on the AstroWind template) carrying the dark "Observer" editorial tone, with Elle, our corpus-grounded intelligence, woven throughout.

- 🔗 **Production:** [ethicalintelligenceproject.pages.dev](https://ethicalintelligenceproject.pages.dev)
- 💬 **Talk to Elle:** [/elle](https://ethicalintelligenceproject.pages.dev/elle)

<br>

## Table of Contents

- [What's inside](#whats-inside)
- [Tech stack](#tech-stack)
- [Getting started](#getting-started)
  - [Requirements](#requirements)
  - [Commands](#commands)
- [Project structure](#project-structure)
- [Configuration](#configuration)
- [Elle integration](#elle-integration)
- [Deploy](#deploy)
- [Acknowledgements](#acknowledgements)
- [License](#license)

<br>

## What's inside

The site presents the project as one presence with nine expressions — the **Nine Engines**:

| #   | Engine                    | Focus                                |
| :-- | :------------------------ | :----------------------------------- |
| 01  | Elle Law                  | Rights & legal reasoning             |
| 02  | Harmonizer                | Mental health & peer support         |
| 03  | Atlas Edu                 | Education & navigation               |
| 04  | Agricultural Intelligence | USDA & farm resources                |
| 05  | Healthcare Navigation     | Benefits & patient rights            |
| 06  | Small Business Hub        | Licensing, grants & compliance       |
| 07  | Civic Intelligence        | Government documents, translated     |
| 08  | RAPID²AI                  | Hospitality operational intelligence |
| 09  | The Observer              | Research & testimony                 |

Alongside the engines, the site surfaces the **corpus** (the intellectual framework Elle reasons from), the project's **AI principles** (transparent, auditable, human-centered, non-extractive, community-governed), ways to get involved, and a full Elle chat experience at `/elle`.

<br>

## Tech stack

- **[Astro v6](https://astro.build/)** — static site generation
- **[Tailwind CSS v4](https://tailwindcss.com/)** — CSS-first styling
- **TypeScript** · **MDX** · **Sharp** (image optimization)
- **Elle** — corpus-grounded intelligence served via a Cloudflare Worker (`elle-worker`)

<br>

## Getting started

### Requirements

- **Node.js >= 22.12.0**

Install dependencies:

```shell
npm install
```

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

> **Note:** `npm run check` is what CI runs. Run `npm run fix` before committing to keep Prettier and ESLint green.

<br>

## Project structure

```
/
├── public/
├── src/
│   ├── assets/styles/tailwind.css   # Tailwind v4 theme tokens & utilities
│   ├── components/
│   │   ├── common/                  # Image, Metadata, Analytics, ToggleTheme
│   │   ├── ui/                       # Button, Headline, WidgetWrapper, ItemGrid
│   │   ├── widgets/                  # Hero, Features, Pricing, Header, Footer
│   │   └── CustomStyles.astro        # CSS variables for colors and fonts
│   ├── content.config.ts             # Content Collections schema
│   ├── data/post/                    # Blog posts (.md, .mdx)
│   ├── layouts/                      # Layout, PageLayout, MarkdownLayout
│   ├── pages/                        # File-based routing
│   │   ├── index.astro               # Homepage (Observer tone, Nine Engines)
│   │   ├── elle.astro                # Talk to Elle — chat experience
│   │   └── ...                       # about, services, pricing, contact, blog, landing
│   ├── config.yaml                   # Site configuration (virtual module)
│   └── navigation.ts                 # Header & footer navigation
├── astro.config.ts
└── package.json
```

Astro looks for `.astro` or `.md` files in `src/pages/`; each file becomes a route based on its name. Static assets that need no transformation live in `public/`; assets imported directly live in `src/assets/`.

<br>

## Configuration

Site-wide configuration lives in `src/config.yaml` (loaded as the virtual module `astrowind:config`). The branding, SEO metadata, and analytics are set there:

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
- `src/pages/index.astro` — the homepage's self-contained dark "Observer" styles (scoped under `#tep`)

<br>

## Elle integration

Elle is served by an external Cloudflare Worker. The homepage loads the floating chat widget, and `/elle` is the full conversation experience:

- **Widget:** `https://elle-worker.sbarteau2022.workers.dev/widget.js`
- **Chat / auth endpoints:** `/api/widget-chat`, `/api/elle-conversation`, `/api/elle-auth`

Guests get corpus-aware answers; signed-in users get full corpus reasoning and persistent memory.

<br>

## Deploy

The site builds to static files in `dist/` and can be hosted anywhere. It is configured for **Cloudflare Pages**, **Netlify** (`netlify.toml`), and **Vercel** (`vercel.json`).

```shell
npm run build
```

> **Cloudflare Pages / Netlify / Vercel:** set the build command to `npm run build` and the output directory to `dist`. Avoid calling `vite`/`astro` binaries directly as the build command — use the `package.json` script so the locally installed CLI is found.

<br>

## Acknowledgements

Built on the [AstroWind](https://github.com/arthelokyo/astrowind) template, originally created by **Arthelokyo** and maintained by its community of contributors. Elle's corpus is co-authored with Claude (Anthropic).

## License

Licensed under the MIT license — see the [LICENSE](./LICENSE.md) file for details.
