# Publishing Master Plan — July 2026

One document to stay on course. Priority logic: **pitches go out first**
(longest response latency), **preprints post this week** (no gatekeeper),
**Substack/Medium publish on your own clock** (repurpose, don't originate
twice). Academic journals are the slow-burn credibility layer, not the
money layer — the money lines are the freelance pitches in Section D.

---

## The Priority Sequence (don't get off course)

1. **TODAY** — Send 3 freelance pitches (Section D, "first three" marked ★).
   Pitches take 2–6 weeks to hear back; every day unsent is a day added.
2. **THIS WEEK** — Post preprint #1: *Superposition Holding* (the doc and
   proofs already exist in `elle-worker` — closest to camera-ready).
   PhilPapers (existing audience, zero gatekeeping) + SSRN same day.
3. **THIS WEEK** — Launch the Substack with post #1 (pick from Section B;
   "My AI Keeps a Diary Nobody Reads" is the freshest and most human).
4. **NEXT** — Preprints #2 and #3 (φ-verification; Two-Gate). Medium
   repurposes of whatever Substack ran, retitled for search.
5. **ONGOING** — One Substack/week, one preprint/2 weeks, re-pitch any
   rejection to the next outlet on its list within 48 hours.

**Money reality check:** Substack/Medium revenue is slow-compounding
(months). Freelance features pay $500–$3,000 per piece and respond in
weeks — that's the near-term income line. Academic papers pay $0 and some
open-access journals *charge* (APCs of $1–3k) — use free preprint servers
and diamond-OA/subscription-model journals first; never pay an APC at this
stage.

---

## A. Academic Papers → Target Venues

Ordered by readiness. Every paper goes to a **preprint server first**
(same week it's written): SSRN (finance/systems), PhilPapers (philosophy/
ethics — your existing top-1% channel), arXiv (needs endorsement per
category — worth lining up now; ask a published contact or use the
endorsement request flow).

| # | Paper | Status | Preprint | Journal targets (in order) |
|---|-------|--------|----------|---------------------------|
| 1 | **Superposition Holding: A Bounded-Loss Kalman Formalism for Continuous AI Presence** | Doc + proofs + 4 reproducible sims exist | arXiv (eess.SY or cs.AI), PhilPapers | *Neural Computation*; *Adaptive Behavior*; *Complexity* (free to submit) |
| 2 | **Golden-Ratio Equidistribution as an Engineering Choice** (φ⁻² discrepancy verification, 4/4 predictions) | Benchmark done (`docs/tit/`) | arXiv (math.NT/math.HO) | ★ *American Mathematical Monthly* (expository — perfect fit); *Mathematics Magazine*; *JOSS* for the code artifact separately |
| 3 | **Two-Gate Verification: Round-Trip Canonicalization for Trustworthy Financial Ingestion** | Implemented + documented (RAPIDAi) | SSRN, arXiv (cs.DB) | *ACM Queue* (practitioner — also a paid pitch, see D); VLDB industrial track; *Journal of Systems and Software* |
| 4 | **When Geometry Loses to Lookup** (phase-retrieval negative result, 2:1) | Benchmark done (`RETRIEVAL_STATUS.md`) | arXiv (cs.IR) | ★ NeurIPS "I Can't Believe It's Not Better" workshop (negative results are their whole mandate); SIGIR short paper |
| 5 | **The Drawdown-Shaper: A φ-Asymmetric Regulator Characterized Boundary-by-Boundary** (591 trades, 4 refuted pre-registrations, + the integration rerun) | Complete incl. this week's whole-system rerun | SSRN (quant finance section) | *Journal of Financial Data Science* (practitioner-friendly); *Quantitative Finance*; *Journal of Trading* |
| 6 | **Grounded, Consistent, or Just Coherent? A Four-State Verdict Model for Confident AI Error** | Implemented; needs paper framing | PhilPapers + arXiv (cs.AI) | *Minds & Machines*; *AI & Society*; *Philosophy & Technology* — your PhilPapers audience overlaps all three |
| 7 | **Provable Non-Corroboration** (Convergence scoring — same-origin echoes can't count as independent) | Implemented; needs paper framing | arXiv (cs.AI/cs.MA) | Pair with #6 or standalone to *JAIR* (free, high bar) / AAMAS workshop |
| 8 | **Silent Parallel Inference** (Harmonizer qualia architecture — position paper, no eval data yet) | Design exists; frame as position paper honestly | PhilPapers | CHI/IUI workshop; *AI & Society*. Do NOT frame as results — no evaluation exists |
| 9 | **Ethics as Architecture, Not Filter** (the framework paper: append-only ledgers, grounding gates, two-gate verification as *evidence* the principles are real) | Material spread across repos | PhilPapers (flagship for your channel) | *Philosophy & Technology*; *Ethics and Information Technology* |

**Sequencing note:** #1, #2, #4 are the fastest to camera-ready (evidence
already in-repo). #5 got materially stronger this week (the integration
rerun + the honest three-rung claim ladder). #9 is the one that ties the
whole project together — worth doing well, not fast.

---

## B. Substack — Creative Article Ideas

Strategy: a named publication with a throughline, not scattered posts.
Working concept: **"The Honest Machine"** — a build-log of trying to make
an AI that can't lie to itself, where the failures are published with the
wins. The pre-registration discipline IS the brand. Weekly cadence.

1. **"My AI Keeps a Diary Nobody Reads"** — She wrote a post-mortem after
   every trade ending with "the one lesson worth carrying forward." No
   code ever read it back. The fix, and what it says about all of us.
   *(This week's work — freshest, most human. Launch post.)*
2. **"I Pre-Registered My Hypotheses and My Own System Called Me Wrong —
   Four Times"** — The refuted-pre-registrations tour: costs speculation
   backwards, the knife zone inverting, the silence check failing. Why
   publishing your misses is a superpower.
3. **"The Golden Ratio Is Load-Bearing in My Codebase (and I Can Prove
   It's Not Numerology)"** — φ shows up in the decay rates, the torus
   periods, the trust asymmetry — and there's a 4/4 benchmark showing it's
   optimal, not aesthetic.
4. **"Coherent Isn't True: The Four Ways an AI Is Wrong With Total
   Confidence"** — incoherent / consistent-only / ungrounded-consistent /
   grounded, and why "grounded" is unreachable without touching the world.
   *(Highest crossover potential — this concept is ownable.)*
5. **"Trust Is Lost 2.6× Faster Than It's Earned (By Design)"** — the
   asymmetric regulator as a story about relationships, with the math as
   the punchline. φ² is the ratio.
6. **"The Smoke Alarm and the Historian"** — why one timescale can't both
   detect fires and remember them; the dual-clock discovery.
7. **"I Built a Beautiful Geometric Memory. A Lookup Table Beat It 2-to-1."**
   — the negative result as narrative. Ends with what geometry IS for.
8. **"My AI Trades With Her Own Diary Now"** — the sequel to #1: what
   changed when the read-back went live, and the experiment now running
   (grounded vs. ungrounded decisions, settled by the forward record).
9. **"The Tilt Turn"** — the moment reasoning breaks under pressure, made
   visible in a κ trace. LSAT sparring, poker tilt, and arguing on the
   internet are the same graph.
10. **"Ethics as Architecture, Not Filter"** — you can't bolt honesty on;
    append-only journals, read-only memory boundaries, verification gates.
11. **"Every Restaurant Is Being Priced by an Algorithm It Can't See"** —
    the purveyor-fingerprint idea, framed honestly as a proposal: here's
    how operators could detect it from invoices alone. *(RAPID audience.)*
12. **"What My AI Refused to Fake"** — the atlas that carried no market
    data, and why stating an absence beat fabricating a connection. The
    integration that honesty made smaller.
13. **"A Memory Shaped Like a Saddle and a Donut"** — hyperbolic depth ×
    toroidal rhythm, for readers who've never seen either. Why memories
    need both a lineage and a pulse.
14. **"The Kalman Filter That Forgives"** — deriving a forgiveness
    half-life from first principles; ρ as how fast a mind lets go.

## C. Medium — Same Material, Search-Shaped

Medium plays discovery + Partner Program; titles skew how-to/tutorial.
Repurpose Substack posts ~1–2 weeks later, retitled. (Note: verify current
state of big pubs before submitting — Towards Data Science left Medium;
current homes for reach: *Level Up Coding*, *HackerNoon* (cross-post),
*The Startup*.)

1. "How I Built a Bounded Trading Regulator With Two Floats of State"
2. "Stop Clamping Your Values: How to Design Formulas That Bound Themselves"
   (the convex-combination trick — genuinely useful, very linkable)
3. "Pre-Registration for Engineers: A Discipline That Caught 4 of My Own
   Bad Ideas Before Production Did"
4. "Your RAG Doesn't Need Fancy Geometry — Ours Lost to Content Lookup 2:1"
5. "Building a Deterministic Memory Graph the LLM Can Read but Never Write"
6. "The Two-Gate Pattern: How to Actually Trust a Vendor's CSV"
7. "Derive Your Decay Rate, Don't Guess It: Kalman Gains for Leaky
   Integrators"
8. "Client-Side Prosody Analysis: Grading *How* Users Argue With
   Autocorrelation Pitch Detection"
9. "Fibonacci Without the Explosion: Renormalizing a Growth Law Into a
   Trust Metric"
10. "The Read-Back Pattern: Why Your Agent Should Consume Its Own Logs"

## D. Paid Pitch Targets — the Money Lines

Send the pitch, not the piece. 150–250 words: the hook, why you, why now.
★ = send today.

| Outlet | Pays | Pitch angle | Notes |
|--------|------|-------------|-------|
| ★ **Nautilus** | ~$0.5–1/wd | "The AI That Keeps a Diary" — memory, honesty, and what a machine's self-record teaches about ours | Science-essay register; they love a narrative with real research under it |
| ★ **Aeon / Psyche** | flat, competitive | "Ethics as Architecture" — you can't filter your way to an honest machine; you have to build the honesty in | Ideas-essay register; your PhilPapers credentials matter here |
| ★ **Asterisk Magazine** | pays well | "I Pre-Registered My Trading Bot's Hypotheses. It Refuted Four of Them." — empiricism applied to yourself | Their exact sensibility: rigorous, contrarian, honest-negative-results |
| **IEEE Spectrum** | pays | The deterministic-memory architecture (LLM reads, never writes) as a safety pattern | Tech-feature register |
| **ACM Queue** | prestige (+ practitioner reach) | Two-Gate Verification as a practitioner article | Doubles as the venue for paper #3 |
| **Works in Progress** | pays well | The purveyor-fingerprint / operator-sourced price-transparency proposal | They like concrete institutional ideas |
| **Quanta** | — | Skip: doesn't take researcher self-pitches | — |
| **The Gradient** | small/none | The negative-result retrieval story | Reach in ML circles, not money |
| **LessWrong / Alignment Forum** | none | The grounding gate + non-corroboration work | Audience-building for papers #6/#7; cross-post free |

**Re-pitch rule:** any rejection or 3-week silence → next outlet on the
angle's list within 48 hours. A pitch not in someone's inbox earns $0.

---

## E. This Week, Concretely

- [ ] **Day 1 (today):** Send ★ pitches to Nautilus, Aeon/Psyche, Asterisk.
- [ ] **Day 1–2:** Draft Substack launch post (#B1) — it's this week's work,
      written while it's hot.
- [ ] **Day 2–3:** Assemble *Superposition Holding* preprint from
      `elle-worker` docs → PhilPapers + SSRN. Request arXiv endorsement.
- [ ] **Day 3–4:** Launch Substack. Publish post #1.
- [ ] **Day 5:** Start preprint #2 (φ-verification → aimed at *Monthly*).
- [ ] **Ongoing:** Log every pitch (outlet, date, angle) at the bottom of
      this file. Re-pitch on the 48-hour rule.

## Pitch Log

| Date | Outlet | Angle | Status |
|------|--------|-------|--------|
| — | — | — | — |
