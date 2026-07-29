# vendor/

Local (non-npm) code that the site depends on directly.

## `integration/`

A custom Astro integration (`vendor/integration/`) that loads `src/config.yaml`
and exposes it to the rest of the site as the virtual module `astrowind:config`
(`SITE`, `I18N`, `METADATA`, `APP_BLOG`, `UI`, `ANALYTICS`). It's registered in
[`astro.config.ts`](../astro.config.ts):

```ts
import astrowind from './vendor/integration';

export default defineConfig({
  integrations: [
    // ...
    astrowind({ config: './src/config.yaml' }),
  ],
});
```

It also appends the generated `sitemap-index.xml` URL to `public/robots.txt`
after each build (`astro:build:done`).

Files:

- `index.ts` — the integration itself (`astro:config:setup`, `astro:build:done` hooks).
- `utils/loadConfig.ts` — reads and parses `src/config.yaml`.
- `utils/configBuilder.ts` — turns the raw YAML into the typed `SITE`/`I18N`/`METADATA`/`APP_BLOG`/`UI`/`ANALYTICS` config objects.
- `types.d.ts` — shared types for the integration.

This is vendored (kept in-repo rather than published to npm) because it's
specific to this site's config shape; see [`AGENTS.md`](../AGENTS.md) for the
broader AstroWind conventions it plugs into.
