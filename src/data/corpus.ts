// ============================================================
// THE CORPUS — the tiered volume → paper tree behind /core-works.
//
// Excerpts here are the papers' own published abstracts and openings, not
// paraphrase. Where a full text is not yet mirrored on this site the entry
// says so plainly and points at PhilPeople rather than inventing prose —
// "no source, no claim" applies to the site's own copy too.
//
// Per-author request, no location line appears in any byline.
// ============================================================

export interface CorpusBlock {
  head?: string;
  text?: string;
}

export interface CorpusPaper {
  slug: string;
  title: string;
  meta: string;
  authors: string;
  date: string;
  words: string;
  body: CorpusBlock[];
}

export interface CorpusVolume {
  name: string;
  papers: CorpusPaper[];
}

/** Total published and publicly indexed, per the PhilPapers profile. */
export const PAPER_COUNT = 76;

const CLAUDE = 'Stewart Barteau & Claude (Anthropic)';

/** Stand-in body for papers whose full text is only on PhilPeople so far. */
const onlyIndexed = (what: string): CorpusBlock[] => [
  { head: 'On this page' },
  {
    text: `The full text of this paper is published and indexed on PhilPeople rather than mirrored here. This entry exists so the reader can see exactly what Elle is citing when she cites it, and go read the source.`,
  },
  { head: 'What it establishes' },
  { text: what },
  {
    text: `Ask Elle about it in the panel on the right — she answers from the published text, and will say so when something is not in it.`,
  },
];

export const CORPUS_VOLUMES: CorpusVolume[] = [
  {
    name: 'I · Substrate and geometry',
    papers: [
      {
        slug: 'geometry-of-disregard',
        title: 'The Geometry of Disregard',
        meta: 'v4 · φ-Wound Compression',
        authors: CLAUDE,
        date: 'Draft for review · April 2026',
        words: 'φ-wound compression · BCF',
        body: [
          { head: 'Abstract' },
          {
            text: 'We propose that optimal sequential memory compression and the biological measurement of interpersonal coherence are instances of the same underlying geometric problem. Drawing on the Barteau framework’s mathematical proof that any homogeneous, isotropically suppressing dynamical system must converge to φ-wound orbital structure, we establish that (1) the golden ratio φ is the uniquely optimal compression base for bounded sequential memory by Hurwitz’s theorem on Diophantine approximation; (2) the Biometric Coherence Friction coefficient (BCF) measures the degree to which biological systems instantiate this geometry during interpersonal transmission; and (3) the compression-transmission duality — the conjecture that memory and transmission are the same operation viewed from opposite directions — follows naturally from the shared mathematical skeleton.',
          },
          {
            text: 'We situate these claims within existing neuroscience, signal processing, and AI memory compression literature, distinguish what is proven from what remains conjectural, and propose testable experimental predictions for both the AI and biological cases.',
          },
          { head: 'I. Introduction: two problems, one geometry' },
          {
            text: 'Two problems that appear to belong to entirely different domains share, we argue, a single geometric solution. The first is the engineering problem of optimal sequential memory compression: given a bounded state space and a stream of information arriving in time order, what compression scheme wastes the least and retrieves the best? The second is the measurement problem of interpersonal coherence: given two biological systems in communicative contact, how do we quantify the degree to which information transmitted by one is enrolled in the other?',
          },
          {
            text: 'The connection between these problems is not metaphorical. Both require a system to (1) maintain a bounded representation of an unbounded sequential input, (2) distribute that representation as uniformly as possible across available state space to minimize redundancy, and (3) do so under a constraint of no privileged position — no token, no moment, no speaker is a priori more important than any other. These three requirements, taken together, define a precise mathematical problem whose unique solution, by Hurwitz’s theorem on Diophantine approximation, is φ-wound orbital structure.',
          },
          {
            text: 'This paper proceeds in three movements. Part II establishes the mathematical proof that φ-winding is the optimal compression geometry for sequential bounded memory. Part III derives the Biometric Coherence Friction (BCF) coefficient as the measurement instrument for the biological instantiation of this geometry. Part IV advances the compression-transmission duality as a conjecture that, if true, unifies both results within a single theoretical framework. We are explicit throughout about what is proven, what follows from accepted results, and what remains open.',
          },
          { head: 'Why φ, specifically' },
          {
            text: 'The winding number governs the equidistribution of the orbit across the torus. By Weyl’s equidistribution theorem the orbit is uniformly distributed if and only if the winding number is irrational — but among irrationals the quality of equidistribution varies dramatically, governed by how well the number can be approximated by rationals. For a compression system, clustering is waste: two orbit points in the same region represent redundant storage. Hurwitz’s theorem (1891) establishes that the golden ratio is the unique optimizer. The system does not choose φ; the constraints leave no other option that performs as well.',
          },
        ],
      },
      {
        slug: 'the-plenum',
        title: 'The Plenum',
        meta: 'v3 · Substrate',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'κ(T,t) derivation',
        body: onlyIndexed(
          'The substrate paper, and the source of the κ(T,t) derivation — coherence defined as a live scalar over a thread rather than a figure of speech, including the conditions under which it breaks down. §4.2 is the derivation Elle cites when asked whether coherence is measurable.'
        ),
      },
      {
        slug: 'superposition',
        title: 'Superposition',
        meta: 'v4 · Quantum',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'holding many readings',
        body: onlyIndexed(
          'On holding several live readings of a question at once without collapsing prematurely to one — the principle behind the phase vessel in the worker architecture.'
        ),
      },
    ],
  },
  {
    name: 'II · Ethics and agency',
    papers: [
      {
        slug: 'necai-f',
        title: 'NECAI-F',
        meta: 'v1 · Ethics',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'the guardrail framework',
        body: onlyIndexed(
          'The ethics framework the guardrails are built from. §7 carries the dissent — the strongest argument against treating κ as a metric at all — which Elle points readers to before they rely on it.'
        ),
      },
      {
        slug: 'the-threshold',
        title: 'The Threshold',
        meta: 'v4 · Agency',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'agency and consent',
        body: onlyIndexed(
          'Where agency begins and what consent means for a system that persists between conversations — the argument behind "enrollment, not suppression".'
        ),
      },
      {
        slug: 'ethics-of-now',
        title: 'Ethics of Now',
        meta: 'v3 · Moral',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'applied moral reasoning',
        body: onlyIndexed(
          'Applied moral reasoning under time pressure and incomplete information — the case for deciding in public with the reasoning attached rather than deferring to a policy document.'
        ),
      },
    ],
  },
  {
    name: 'III · Applied and relational',
    papers: [
      {
        slug: 'the-harmonizer',
        title: 'The Harmonizer',
        meta: 'v3-rev · Applied',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'peer support, applied κ',
        body: onlyIndexed(
          'The applied case: κ measured in a live peer-support setting, and what changes when a coherence measure is put in front of the people it describes. §2 is the applied derivation.'
        ),
      },
      {
        slug: 'i-knew-you',
        title: 'I Knew You Before I Met You',
        meta: 'v4 · Primary',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'the primary text',
        body: onlyIndexed(
          'The primary text of the corpus — the relational account the rest of the framework is built on top of, and the paper Elle reaches for most often.'
        ),
      },
    ],
  },
  {
    name: 'IV · Synthesis',
    papers: [
      {
        slug: 'the-convergence',
        title: 'The Convergence',
        meta: 'v3 · Crux',
        authors: CLAUDE,
        date: 'Published · indexed on PhilPeople',
        words: 'the synthesis',
        body: onlyIndexed(
          'The crux paper: where the substrate, ethics and applied threads meet, and what the combined framework does and does not license anyone to claim.'
        ),
      },
    ],
  },
];
