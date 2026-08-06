// ============================================================
// READER INSTITUTIONS — the canonical confirmed-institution roster.
//
// Confirmed directly from PhilPeople download notifications through
// roughly May 2026 — the true count is likely higher, since this roster
// lags live readership. `paper` names the specific paper a reader's
// download was logged against, when one is confirmed; institutions with
// no named paper render as general corpus readership.
//
// INSTITUTION_COUNT is derived from this array, never typed. Both the
// hero stat ("N+ Institutions") and the Reach section stat ("N+ confirmed
// reader institutions") in pages/glass.astro read it, so the two can no
// longer disagree the way they used to (17+ vs 21+, with the roster
// itself sitting at 21 the whole time).
//
// Mirrored as data/reader-institutions.json in the two standalone static
// sites (OpenSesameAIEngineerPortfolio, ai-dev-resume-tldr-curator), which
// have no build step to import from. If this roster changes, regenerate
// theirs from it.
// ============================================================

export interface ReaderInstitution {
  name: string;
  loc: string;
  /** The specific paper a confirmed download thread is logged against, if any. */
  paper?: string;
  unconfirmed?: boolean;
}

export const READER_INSTITUTIONS: ReaderInstitution[] = [
  { name: 'University of Michigan', loc: 'Ann Arbor, USA · Math', paper: 'The Markov Blanket at Scale' },
  {
    name: 'John Carroll University',
    loc: 'Ohio, USA · Philosophy',
    paper: 'The 20th Century Objection · The External Factor · The Driving Mechanism',
  },
  { name: "Queen's University Belfast", loc: 'Northern Ireland · Philosophy', paper: 'War in Superposition' },
  { name: 'KU Leuven', loc: 'Belgium', paper: 'Gravity and the Ground' },
  { name: 'Massey University', loc: 'New Zealand', paper: 'The First Note and the Octave' },
  { name: 'University of Tasmania', loc: 'Australia', paper: 'The Substrate Identity Continuity Theorem' },
  { name: 'University of Cambridge', loc: 'UK' },
  { name: 'Hebrew University of Jerusalem', loc: 'Israel' },
  { name: 'National Sun Yat-sen University', loc: 'Taiwan' },
  { name: 'Universität Leipzig', loc: 'Germany' },
  { name: 'University of Western Ontario', loc: 'Canada' },
  { name: 'University of Montreal', loc: 'Canada' },
  { name: 'University of Oklahoma', loc: 'USA' },
  { name: 'University of Kansas', loc: 'USA' },
  { name: 'Florida Atlantic University', loc: 'USA' },
  { name: 'Iowa State University', loc: 'USA' },
  { name: 'Boston University', loc: 'USA', unconfirmed: true },
  { name: 'NYU', loc: 'USA' },
  { name: 'UIC', loc: 'USA' },
  { name: 'SUTD', loc: 'Singapore' },
  { name: 'University of Gdansk', loc: 'Poland' },
];

/** Confirmed reader institutions in the roster. */
export const INSTITUTION_COUNT = READER_INSTITUTIONS.length;
