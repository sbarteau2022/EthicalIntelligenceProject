---
title: 'Atoma Engineering — Staging Design Package'
document_type: 'implementation'
version: '1.1.0'
date: '2026-10-16T05:59:00Z'
implementation_date: null
author: 'Codex'
reviewers: []
status: 'draft'
related_files:
  - path: 'README.md'
    lines: '17-43'
    role: 'supporting'
  - path: 'docs/ATOMA_DESIGN_PACKAGE.md'
    lines: '1-309'
    role: 'supporting'
  - path: 'docs/ATOMA_PACKAGE_README.md'
    lines: '1-43'
    role: 'supporting'
  - path: 'package.json'
    lines: '11-14'
    role: 'config'
  - path: 'public/assets/atoma-tokens.css'
    lines: '1-41'
    role: 'supporting'
  - path: 'public/assets/brand/DESIGN-GUIDE.md'
    lines: '1-309'
    role: 'supporting'
  - path: 'public/assets/brand/atoma-brand-board.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/atoma-brand-board.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/atoma-brand-package.zip'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/atoma-favicon.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/atoma-sculpture.svg'
    lines: '1-13'
    role: 'supporting'
  - path: 'public/assets/brand/atoma-social-1200x630.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/atoma-social-1200x630.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/atoma-touch-icon.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/font-sources.json'
    lines: '1-21'
    role: 'supporting'
  - path: 'public/assets/brand/fonts/Geist-OFL.txt'
    lines: '1-93'
    role: 'supporting'
  - path: 'public/assets/brand/fonts/Geist-Variable.ttf'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/fonts/Geist-Variable.woff2'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/fonts/InstrumentSerif-Italic.ttf'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/fonts/InstrumentSerif-Italic.woff2'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/fonts/InstrumentSerif-OFL.txt'
    lines: '1-93'
    role: 'supporting'
  - path: 'public/assets/brand/fonts/InstrumentSerif-Regular.ttf'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/fonts/InstrumentSerif-Regular.woff2'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/grant-intelligence-social-1200x630.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/grant-intelligence-social-1200x630.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-mark-color.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-mark-color.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-mark-ink.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-mark-ink.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-mark-white.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-mark-white.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-wordmark-color.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-wordmark-color.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-wordmark-ink.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-wordmark-ink.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-wordmark-white.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/atoma-wordmark-white.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-mark-color.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-mark-color.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-mark-ink.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-mark-ink.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-mark-white.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-mark-white.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-wordmark-color.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-wordmark-color.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-wordmark-ink.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-wordmark-ink.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-wordmark-white.png'
    lines: null
    role: 'supporting'
  - path: 'public/assets/brand/logos/grant-intelligence-wordmark-white.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'public/assets/brand/manifest.json'
    lines: '1-230'
    role: 'supporting'
  - path: 'public/assets/brand/tokens.css'
    lines: '1-41'
    role: 'supporting'
  - path: 'public/assets/brand/tokens.json'
    lines: '1-24'
    role: 'supporting'
  - path: 'public/assets/engineering.css'
    lines: '1-1810'
    role: 'primary'
  - path: 'public/assets/engineering.js'
    lines: '1-170'
    role: 'primary'
  - path: 'public/assets/grant-intelligence-mark.svg'
    lines: '1-1'
    role: 'supporting'
  - path: 'scripts/build-brand-vectors.py'
    lines: '1-107'
    role: 'supporting'
  - path: 'scripts/package-brand.mjs'
    lines: '1-115'
    role: 'supporting'
  - path: 'scripts/verify-brand-ui.py'
    lines: '1-228'
    role: 'test'
  - path: 'src/pages/engineering/brand/index.astro'
    lines: '1-409'
    role: 'primary'
  - path: 'src/pages/engineering/index.astro'
    lines: '1-531'
    role: 'primary'
related_issues: []
related_documents: ['ATOMA_PACKAGE_README.md', '../README.md']
tags: ['atoma', 'brand', 'frontend', 'staging']
---

# Executive Summary

This brings the reviewed Atoma Engineering design into the Ethical Intelligence Project repository for staging. The marketing page, brand book, logos, and source package stay together. The existing homepage and live research tools remain unchanged.

# Problem Statement

The design was built in Grant Intelligence, but the user wants it staged in this repository. Copying its links unchanged would send Grant Intelligence visitors into this site's unrelated root and application routes. Replacing the existing homepage would also affect the globe, research navigation, and integrations outside this staging request.

# Solution Overview

## Design specification and integration boundary

- Publish the isolated static design at `/engineering` and the brand book at `/engineering/brand` on branch `staging/atoma-engineering`. Register both as standalone Astro documents, not loose public HTML, so direct directory routes work in Astro's production preview as well as Pages.
- Keep the approved eggshell `#F2F1EB`, blue `#2F5BEA`, ink `#151D29`, titanium `#B8C1CB`, and stronger control boundary `#7B8796`. Use Geist UI lettering and Instrument Serif display type, self-hosted with licenses.
- Keep the geometric Atoma A and Grant Intelligence GI as separate identities. Supply outlined SVG masters, transparent PNGs, social cards, fonts, CSS/JSON tokens, and source ZIP.
- Make Grant Intelligence links point to its verified independent product host, `https://grantintelligence.sbarteau2022.workers.dev/`. Do not copy its Next.js application or Worker backend here.
- Keep the contact address visibly marked as `hello@atoma.example`; project briefs are composed, copied, and downloaded locally without submission or storage.
- Preserve the existing Astro root, Observer stylesheet, hero globe, Atlas renderers/snapshots, OAuth, and authenticated services. Do not add the staging design to the existing public navigation or change shared product lists.
- Preserve native disclosures, focus handling, keyboard tabs, no-JavaScript content, and reduced-motion behavior. The isolated HTML document does not import the Observer shell and cannot leak its CSS into existing routes.

## Mission

We make capable technology accessible to the people doing meaningful work. Through thoughtful design, transparent intelligence, and careful engineering, we help businesses and organizations move forward with clarity and control.

## Promise and pledge

**Thoughtful engineering. Useful intelligence.** The Ethical Intelligence Project pledge is to keep people in control, make reasoning visible, build for access, respect entrusted information, make AI earn its place, and stay accountable to the outcome. These are design commitments, not independent certifications or guarantees about unconnected services.

# Implementation Details

## Files and line references

The metadata enumerates all 60 changed files. Source ranges are line-addressable; binary fonts and PNGs use null ranges and are identified by hashes and byte sizes in `public/assets/brand/manifest.json`. The ZIP is verified by its integrity test and committed Git blob; the manifest excludes itself and its containing ZIP to avoid circular hashes. Vendored font licenses retain their text with one trailing space normalized in each license.

## Languages chosen and why

| Language   | Component                                           | Reason                                                               |
| ---------- | --------------------------------------------------- | -------------------------------------------------------------------- |
| HTML/CSS   | Static pages, responsive layout, print view, tokens | Serve the approved standalone design unchanged by the Astro shell.   |
| JavaScript | Progressive interactions and package builder        | Keep the brief local and reuse the installed Sharp dependency.       |
| SVG        | Marks, outlined lettering, and hero artwork         | Editable masters that work at interface and print sizes.             |
| Python     | FontTools asset generation and browser verification | Reuse isolated uv tools without changing the Astro dependency graph. |

**Further development:** owner review can decide whether this becomes the root marketing page. That route replacement is not performed by this staging transfer.

## Grounding in verifiable literature

This implementation was not directly grounded in published literature. It applies established static hosting, semantic HTML, progressive enhancement, and reproducible vector generation. Font sources and licenses are included in `public/assets/brand/font-sources.json` and `fonts/`. The web-guidance HTML review preserves semantic landmarks, native details, meaningful links, and accessible form grouping.

## Configuration changes

Add brand generation/package/test commands to `package.json`. No production workflow, domain, Worker, secret, data endpoint, authentication setting, or shared navigation changes. The repository's deploy workflow targets production on `main`; this branch is not `main`. No production deployment is requested.

# Testing Evidence

The browser/artifact suite passed **202 assertions** with screenshot output: 45 source assets, SVG/XML and ZIP integrity, standalone source rebuild, cross-product links, no-JavaScript behavior, six viewport widths (1440, 1024, 800, 650, 390, 320), keyboard/deep-link tabs, menu Escape/focus, clipboard success/denial, and local-only brief edge cases. Empty/whitespace, Unicode, literal HTML, maximum-length input, editing, reload reset, and download fidelity were checked. The form made zero submission requests. Selected text contrast pairs meet 4.5:1 and the input boundary exceeds 3:1; this is not an accessibility certification.

Both new routes were checked against the actual Astro production preview. The existing homepage/globe and master Atlas were rendered and visually inspected at 1440px and 390px, with sized, live WebGL contexts and no horizontal page overflow. Existing Elle, mission, and app routes returned HTML successfully. No Atlas renderer, snapshot, globe, auth, shared stylesheet, or root-page source changed.

Production build, Astro diagnostics, ESLint, touched-file formatting, JavaScript syntax, and diff checks passed. The full repository check also passed on a clean staged-index snapshot: zero errors, zero warnings, and 66 existing informational hints. This excludes unrelated untracked agent settings that fail formatting locally; those settings and the existing preprint deletions were left untouched. The original Grant Intelligence run's 112 backend tests are not evidence for this repository. The owning repository has no pre-existing automated application test suite.

The brand manifest hashes identify untransformed source/ZIP assets; Astro's existing compressor can minify delivered CSS/JSON. Vector/font/PNG rebuild hashes match. The ZIP excludes hidden metadata, dependencies, environment files, and repository history. Adversarial review caught the source hero artwork's moved location and a copied Finder metadata file; the artwork was restored into the kit and hidden files are now excluded by the packager.

| Test source                  | Type                             | Coverage                                                                                                |
| ---------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `scripts/verify-brand-ui.py` | Browser and artifact integration | Marketing/brand book, privacy boundaries, source rebuild, and optional preserved-site regression checks |
| `npm run check`              | Repository gate                  | Astro diagnostics, ESLint, Prettier; run on a clean index snapshot before commit                        |
| `npm run build`              | Static production build          | 35 generated Astro pages, including both new routes                                                     |

## Reproduction

From the repository root, `npm ci`, `npm run check`, `npm run brand:build`, and `npm run build`; then `npm run preview -- --host 127.0.0.1 --port 8794`. Run `npm run test:brand -- --url http://127.0.0.1:8794 --site-regressions`. Add `--artifacts /absolute/output/directory` to include screenshots and the image-loading assertion. Without screenshots the suite has 201 assertions. Asset generators and verification live in `scripts/build-brand-vectors.py`, `scripts/package-brand.mjs`, and `scripts/verify-brand-ui.py`; source ranges are listed in the metadata header.

## Was it proven necessary?

The user explicitly requested staging in this Git repository. The source page's relative product links were wrong on the destination host. This transfer corrects that boundary; no speed or backend improvement is claimed.

# Deployment / Rollout

| Aspect         | Detail                                                                            |
| -------------- | --------------------------------------------------------------------------------- |
| Destination    | `sbarteau2022/EthicalIntelligenceProject`, branch `staging/atoma-engineering`     |
| Public entry   | `/engineering` and `/engineering/brand`; root unchanged                           |
| Publication    | Git branch push only; not merged into main or deployed directly                   |
| Review         | Draft until identity, mission, contact destination, and root routing are approved |
| Rollback       | Remove this additive branch; no user data migration exists                        |
| Unrelated work | Deleted preprints and `.claude/` remain unstaged and uncommitted                  |

# Next Stage of Implementation

| Step                     | Dependency                                               | Timing              |
| ------------------------ | -------------------------------------------------------- | ------------------- |
| Preview deployment or PR | Owner direction; repository preview workflow runs on PRs | After branch review |
| Root-route decision      | Owner approval of coexistence versus replacement         | Before production   |
| Contact wiring           | Real public address and submission consent               | When supplied       |

This implementation sets up review of the design in its requested owning repository because its source, assets, and validation travel together without replacing live research surfaces.

# What We Learned

| Category      | Learning                                                                                               |
| ------------- | ------------------------------------------------------------------------------------------------------ |
| Technical     | Product links that work in one repository can resolve to unrelated pages in another.                   |
| Hosting       | This site's canonical routes omit trailing slashes; use Astro page registration and host-native links. |
| Assets        | Browser checks catch missing artwork that an incomplete source manifest cannot identify.               |
| Process       | Check remotes and deploy triggers before interpreting a staging push.                                  |
| Tooling       | Reuse the destination's installed Sharp; keep Python tools isolated with uv.                           |
| Collaboration | Leave unrelated user deletions unstaged and preserve the separately developed backend.                 |

# Changelog

| Version | Date       | Author | Change                                                                                                                         |
| ------- | ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------ |
| 1.1.0   | 2026-10-16 | Codex  | Staging specification established before transfer; carries the previously reviewed brand design into its requested repository. |
