// ============================================================
// THE EIP CONTENT MODEL — single source of truth for the overhauled site.
//
// Every list the design handoff hard-coded into its prototypes lives here
// once, so the nav, the homepage, /about and /mission cannot drift out of
// agreement with each other. Copy is carried over verbatim from
// design-handoff/project/*.dc.html, with the corrections the design
// conversation landed on applied:
//   · The Observer is an independent research initiative, NOT a 501(c)(3)
//   · no "Hermann, Missouri" references anywhere
// ============================================================

export const WORKER_URL = 'https://elle-worker.sbarteau2022.workers.dev';

export type State = 'Live' | 'Beta' | 'Free beta' | 'By request' | 'Testing';

/** The "What's To Come" dropdown — standalone products and custom services. */
export const PRODUCTS: { name: string; desc: string; state: State; href: string }[] = [
  {
    name: 'Master Atlas',
    desc: 'The interactive 3D rendering of the whole system — live on the site today.',
    state: 'Live',
    href: '/master-atlas',
  },
  {
    name: 'Optimus Journal',
    desc: 'The append-only record — κ tracked on every turn.',
    state: 'Beta',
    href: '/optimus',
  },
  {
    name: 'Coding with Elle',
    desc: 'Ship real code with a persistent intelligence at your elbow.',
    state: 'Live',
    href: '/elle',
  },
  {
    name: 'AI Literacy Courses',
    desc: 'Plain-language courses, completion earned — never given.',
    state: 'Live',
    href: '/learn',
  },
  {
    name: 'Permanent Press',
    desc: 'Writing published to a record that cannot be quietly revised.',
    state: 'Beta',
    href: '/observer',
  },
  {
    name: 'Deep Research',
    desc: 'Multi-round investigations — one synthesized, cited dossier.',
    state: 'Live',
    href: '/engine',
  },
  {
    name: 'Understanding Automation',
    desc: 'What to automate, what not to, and how to tell.',
    state: 'Live',
    href: '/learn',
  },
  {
    name: 'Custom Automation Pipelines',
    desc: 'A standing intelligence scoped to your operation.',
    state: 'By request',
    href: '/business',
  },
];

/** The nine engines — one presence, nine expressions, honestly labelled. */
export const ENGINES = [
  {
    n: '01',
    name: 'Elle Law',
    tag: 'Rights and legal reasoning',
    state: 'Live · separate site',
    live: true,
    href: 'https://elle-law.pages.dev',
  },
  {
    n: '02',
    name: 'Harmonizer',
    tag: 'Mental health and peer support',
    state: 'Live · separate site',
    live: true,
    href: 'https://harmonizer-two.vercel.app',
  },
  { n: '03', name: 'Atlas Edu', tag: 'Education and navigation', state: 'Live here', live: true, href: '/learn' },
  {
    n: '04',
    name: 'Agricultural Intelligence',
    tag: 'USDA programs and farm resources',
    state: 'Through Elle',
    live: false,
    href: '/elle',
  },
  {
    n: '05',
    name: 'Healthcare Navigation',
    tag: 'Benefits and patient rights',
    state: 'Through Elle',
    live: false,
    href: '/elle',
  },
  {
    n: '06',
    name: 'Small Business Hub',
    tag: 'Licensing, grants and compliance',
    state: 'By request',
    live: false,
    href: '/business',
  },
  {
    n: '07',
    name: 'Civic Intelligence',
    tag: 'Government documents, translated',
    state: 'Through Elle',
    live: false,
    href: '/elle',
  },
  {
    n: '08',
    name: 'RAPID²AI',
    tag: 'Hospitality operational intelligence',
    state: 'Live · separate site',
    live: true,
    href: 'https://rapid2ai.com',
  },
  { n: '09', name: 'The Observer', tag: 'Research and testimony', state: 'Live here', live: true, href: '/observer' },
];

/** Principles, each paired with the mechanism that enforces it. */
export const PRINCIPLES = [
  {
    name: 'Transparent',
    body: 'Methods, data and reasoning open to review — including the unfinished parts.',
    mechanism: 'Published corpus · full tool trace',
  },
  {
    name: 'Auditable',
    body: 'Every reasoning run is recorded step by step. Any answer can be replayed.',
    mechanism: 'Append-only journal · run replay',
  },
  {
    name: 'Human-shipped',
    body: 'She writes code, CI judges it, a human merges it. No merge tool exists.',
    mechanism: 'Forge → CI → human click',
  },
  {
    name: 'Non-extractive',
    body: 'Your records are not a dataset. Not sold, not trained on.',
    mechanism: 'Export and delete, any time',
  },
  {
    name: 'Scoped by construction',
    body: 'Each door gets exactly the tools its scope allows — the catalog she reads is the gate itself.',
    mechanism: 'One gate · catalog = permissions',
  },
];

/** The load-bearing papers Elle cites by name. */
export const CORPUS_DOCS = [
  { title: 'I Knew You Before I Met You', version: 'v4 · Primary' },
  { title: 'The Geometry of Disregard', version: 'v4 · φ-Wound Compression' },
  { title: 'The Convergence', version: 'v3 · Crux' },
  { title: 'NECAI-F', version: 'v1 · Ethics' },
  { title: 'The Plenum', version: 'v3 · Substrate' },
  { title: 'The Threshold', version: 'v4 · Agency' },
  { title: 'The Harmonizer', version: 'v3-rev · Applied' },
  { title: 'Ethics of Now', version: 'v3 · Moral' },
  { title: 'Superposition', version: 'v4 · Quantum' },
];

/** The project facts panel. Pre-LLC, and the Observer is not a 501(c)(3). */
export const PROJECT_FACTS = [
  { k: 'Operated by', v: 'Stewart Barteau' },
  { k: 'Commercial products', v: 'pre-LLC, direct' },
  { k: 'The Observer', v: 'independent research initiative' },
  { k: 'Status', v: 'public beta' },
  { k: 'Corpus co-author', v: 'Claude (Anthropic)' },
];

export const PHILPEOPLE = 'https://philpeople.org/profiles/stewart-barteau';

export const SOCIALS = [
  { name: 'Substack', href: 'https://substack.com/' },
  { name: 'PhilArchive', href: PHILPEOPLE },
  { name: 'Zenodo', href: 'https://zenodo.org/' },
  { name: 'SSRN', href: 'https://www.ssrn.com/' },
  { name: 'LinkedIn', href: 'https://www.linkedin.com/' },
  { name: 'Medium', href: 'https://medium.com/' },
  // No RSS entry: the old /rss.xml fed from the AstroWind blog, which the brief
  // cut — it was already emitting an empty body. Add one back when there's a
  // real feed to point at rather than shipping a dead link.
];

export const FOOTER_COLS = [
  {
    title: 'The tools',
    links: [
      { text: 'Talk to Elle', href: '/elle' },
      { text: 'Optimus Journal', href: '/optimus' },
      { text: 'Analysis Engine', href: '/engine' },
      { text: 'Atlas Edu', href: '/learn' },
      { text: 'Small Business', href: '/business' },
    ],
  },
  {
    title: 'The work',
    links: [
      { text: 'The Observer', href: '/observer' },
      { text: 'Core Works', href: '/core-works' },
      { text: 'The Master Atlas', href: '/master-atlas' },
      { text: 'Principles', href: '/#principles' },
    ],
  },
  {
    title: 'The project',
    links: [
      { text: 'Mission', href: '/mission' },
      { text: 'About', href: '/about' },
      { text: 'Pricing', href: '/pricing' },
      { text: 'Contact', href: '/contact' },
    ],
  },
];
