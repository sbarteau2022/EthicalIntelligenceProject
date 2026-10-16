---
title: 'Atoma Design Package — Handoff'
document_type: 'implementation'
version: '1.0.0'
date: '2026-10-16T05:30:00Z'
implementation_date: null
author: 'Codex'
reviewers: []
status: 'draft'
related_documents: ['ATOMA_DESIGN_PACKAGE.md']
---

# Atoma Engineering — Design Edition 01

A review-ready identity and marketing package for Atoma Engineering and Grant Intelligence. Owner approval and production publication are not implied.

## Use the artwork

`public/assets/brand/logos/` contains color, ink, and reversed SVG/transparent PNG marks and outlined wordmarks for both brands. `public/assets/brand/manifest.json` lists asset sizes and SHA-256 hashes. Social artwork, the brand board, font masters, WOFF2 fonts, licenses, favicon, and CSS/JSON tokens are alongside them. The source now lives in the Ethical Intelligence Project repository on its Atoma staging branch.

## Preview the website

From the extracted package root, run `python3 -m http.server 8793 --directory public`, then open `http://127.0.0.1:8793/engineering` or `http://127.0.0.1:8793/engineering/brand`. Use the brand book's print action to save a PDF.

This archive contains the parent marketing website, not the separate Grant Intelligence application or its backend. Product links open `https://grantintelligence.sbarteau2022.workers.dev/`. The local brief never submits or stores information. `hello@atoma.example` is a deliberately labeled placeholder, not a working email address.

## Rebuild the assets

Requirements: Node.js 22+, npm, uv, and the `zip` command. Run `npm install`, then `npm run brand:build`. FontTools is resolved in an isolated uv environment; Sharp is pinned in the package manifest. Font masters and their licenses are already included. No font download is required. Run the same build commands in the original repository to update its delivered assets.

## Verify and review

The design specification and validation evidence are in `docs/ATOMA_DESIGN_PACKAGE.md`. Run `uv run scripts/verify-brand-ui.py --url http://127.0.0.1:8793` against this standalone preview. In the Ethical Intelligence repository, use `npm run test:brand -- --url http://127.0.0.1:8794 --site-regressions` against the built Astro preview to also check the preserved homepage/globe and master Atlas. Headless Google Chrome is required. The source-rebuild test reuses installed Sharp dependencies.

Before production: approve the mission and identity, supply the real public contact destination, confirm product URLs, and configure absolute production social metadata. No deployment is included in this package.

## Handoff notes

The website uses semantic HTML, shared CSS tokens, small progressive JavaScript enhancements, native FAQ/menu disclosures, and reduced-motion support. Vector lettering is outlined. Keep logo proportions intact, maintain clear space of one quarter of the mark width, and use the white artwork on dark surfaces. See the brand book for type, color, motion, voice, and component examples.

## Changelog

1.0.0 · 2026-10-16 · Initial local design handoff. Editable source is included; approval remains pending.
