// ============================================================
// THE HUB — single source of truth for hub navigation + socials
// Used by the hub components (HubNav/HubFooter) and navigation.ts
// so the tab list and social profiles are edited in ONE place.
// ============================================================

export const WORKER_URL = 'https://elle-worker.sbarteau2022.workers.dev';

export const HUB_TABS = [
  { text: 'Optimus', href: '/optimus' },
  { text: 'Analysis Engine', href: '/engine' },
  { text: 'Small Business', href: '/business' },
  { text: 'The Observer', href: '/observer' },
];

// Social / publication profiles. The PhilArchive entry points at the live
// PhilPeople profile; the rest are platform roots until profile URLs exist —
// swap each for the real profile URL as accounts are created.
export const SOCIALS = [
  { name: 'Substack', href: 'https://substack.com/', icon: 'substack' },
  { name: 'Facebook', href: 'https://www.facebook.com/', icon: 'facebook' },
  { name: 'LinkedIn', href: 'https://www.linkedin.com/', icon: 'linkedin' },
  { name: 'Medium', href: 'https://medium.com/', icon: 'medium' },
  { name: 'PhilArchive', href: 'https://philpeople.org/profiles/stewart-barteau', icon: 'philarchive' },
  { name: 'Zenodo', href: 'https://zenodo.org/', icon: 'zenodo' },
  { name: 'SSRN', href: 'https://www.ssrn.com/', icon: 'ssrn' },
];
