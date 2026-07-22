import { getPermalink, getAsset } from './utils/permalinks';

export const headerData = {
  links: [
    {
      text: 'Optimus',
      href: getPermalink('/optimus'),
    },
    {
      text: 'Analysis Engine',
      href: getPermalink('/engine'),
    },
    {
      text: 'Small Business',
      href: getPermalink('/business'),
    },
    {
      text: 'The Observer',
      href: getPermalink('/observer'),
    },
    {
      text: 'More',
      links: [
        {
          text: 'Pricing',
          href: getPermalink('/pricing'),
        },
        {
          text: 'About',
          href: getPermalink('/about'),
        },
        {
          text: 'Principles',
          href: getPermalink('/principled'),
        },
        {
          text: 'Services',
          href: getPermalink('/services'),
        },
        {
          text: 'Contact',
          href: getPermalink('/contact'),
        },
        {
          text: 'Terms',
          href: getPermalink('/terms'),
        },
        {
          text: 'Privacy policy',
          href: getPermalink('/privacy'),
        },
      ],
    },
  ],
  actions: [{ text: 'Talk to Elle →', href: '/elle' }],
};

export const footerData = {
  links: [
    {
      title: 'The Hub',
      links: [
        { text: 'Optimus Journal', href: getPermalink('/optimus') },
        { text: 'Analysis Engine', href: getPermalink('/engine') },
        { text: 'Small Business Hub', href: getPermalink('/business') },
        { text: 'The Observer', href: getPermalink('/observer') },
        { text: 'Talk to Elle', href: '/elle' },
      ],
    },
    {
      title: 'Platform',
      links: [
        { text: 'Harmonizer', href: 'https://harmonizer-two.vercel.app' },
        { text: 'Elle Law', href: 'https://elle-law.pages.dev' },
        { text: 'RAPID²AI', href: 'https://rapidai.pages.dev/coo/' },
        { text: 'Corpus (PhilPeople)', href: 'https://philpeople.org/profiles/stewart-barteau' },
      ],
    },
    {
      title: 'Company',
      links: [
        { text: 'About', href: getPermalink('/about') },
        { text: 'Principles', href: getPermalink('/principled') },
        { text: 'Pricing', href: getPermalink('/pricing') },
        { text: 'Contact', href: getPermalink('/contact') },
      ],
    },
  ],
  secondaryLinks: [
    { text: 'Terms', href: getPermalink('/terms') },
    { text: 'Privacy Policy', href: getPermalink('/privacy') },
    { text: 'Design System', href: getPermalink('/design-system') },
  ],
  // Profile URLs are platform roots until the real profiles exist — swap in
  // the account URLs as they're created (PhilArchive already points at the
  // live PhilPeople profile).
  socialLinks: [
    { ariaLabel: 'Substack', text: 'Substack', href: 'https://substack.com/' },
    { ariaLabel: 'Facebook', icon: 'tabler:brand-facebook', href: 'https://www.facebook.com/' },
    { ariaLabel: 'LinkedIn', icon: 'tabler:brand-linkedin', href: 'https://www.linkedin.com/' },
    { ariaLabel: 'Medium', icon: 'tabler:brand-medium', href: 'https://medium.com/' },
    { ariaLabel: 'PhilArchive', text: 'PhilArchive', href: 'https://philpeople.org/profiles/stewart-barteau' },
    { ariaLabel: 'Zenodo', text: 'Zenodo', href: 'https://zenodo.org/' },
    { ariaLabel: 'SSRN', text: 'SSRN', href: 'https://www.ssrn.com/' },
    { ariaLabel: 'RSS', icon: 'tabler:rss', href: getAsset('/rss.xml') },
  ],
  footNote: `
    The Ethical Intelligence Project · Powered by Elle AI · Hermann, Missouri · All rights reserved.
  `,
};
