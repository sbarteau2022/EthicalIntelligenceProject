# Corpus Forge House Format — the standing spec for all papers

**This is memory. Every paper, preprint, and submission package from The
Observer Foundation uses this format.** Reference artifact: _Formed Before
It Became — Noema submission — v2_ (July 2026). Generator:
`corpus_forge.py` in this directory — add a config dict per paper and run
it; do not hand-build submission PDFs.

## The three-part structure

1. **Jacket (page 1).** Letterspaced Poppins Light header lines — house,
   document class + version, date, venue ("THE OBSERVER FOUNDATION /
   PREPRINT • APPLIED SERIES • V1 / JULY 2026 / FOR …"). Title set huge in
   Pagella, broken across lines. Standfirst in Pagella Italic 12.5.
   Labeled field grid (Poppins Medium 6.4 letterspaced labels; Poppins
   Light 8.5 values): AUTHOR / EXTENT (measured, never estimated) / MODE /
   ADDRESSED TO / STATUS. Foot line, letterspaced: "THE OBSERVER
   FOUNDATION · CORPUS FORGE HOUSE FORMAT · HERMANN, MISSOURI".
2. **Colophon (page 2, "DOCUMENT RECORD").** Label/value rows: TITLE,
   AUTHOR, DOCUMENT CLASS, VERSION, DATE, EXTENT, REGISTER, PRIMARY
   VENUE, SUBMISSION MODE, TOPIC FIT, SOURCE DOCUMENTS, VOICE CALIBRATION
   (essays) / EVIDENTIARY BASIS (papers), SUBJECT SYSTEM, STATUS,
   HANDLING, RIGHTS (© Stewart Barteau · Barteau IP Group LLC), and
   **SOURCE FINGERPRINT** — SHA-256 first 128 bits of the canonical
   source file, grouped 4×8 hex in Liberation Mono, with the sentence
   "recompute to verify." The generator computes this at build time; the
   canonical `.md` it fingerprints is emitted alongside the PDF so the
   claim is always true.
3. **Body.** TeX Gyre Pagella 9.5/13.8 justified. Section heads:
   lowercase, letterspaced, Poppins Medium. Running header from page 1 of
   the body: letterspaced "TITLE · STEWART BARTEAU"; body page numbers
   restart at 1. Math lines centered Liberation Mono; tables Pagella with
   hairline grid.

## Fonts

| Role                         | Face                       | Source                                                                                                                      |
| ---------------------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Body, title, colophon values | TeX Gyre Pagella (4 faces) | `apt install fonts-texgyre`; CFF→TTF via fontTools cu2qu (reportlab needs TrueType outlines — see `corpus_forge.py` header) |
| Letterspaced labels/heads    | Poppins Light + Medium     | github.com/google/fonts `ofl/poppins`                                                                                       |
| Technical strings, math      | Liberation Mono            | system                                                                                                                      |

Letterspacing is implemented as literal thin joining (`A U T H O R`),
matching the reference artifact's extraction behavior.

## Per-venue variation

Only the **jacket lines, jacket fields, and colophon rows** change per
venue; the body format never does. Essays add VOICE CALIBRATION and
COVERING NOTE sections (see the Noema reference); technical papers add
EVIDENTIARY BASIS. Internal back matter (submission ladders, editorial
notes) does not travel with essay submissions; preprints post whole —
record the choice in the HANDLING row.

## Existing builds

- `SUPERPOSITION_HOLDING_preprint.pdf` — preprint #1 (PhilPapers + SSRN),
  built from `SUPERPOSITION_HOLDING_source.md` via the intermediate docx;
  canonical fingerprinted source `SUPERPOSITION_HOLDING_PREPRINT.md`.
  The `.docx` sibling is the SSRN-upload alternative (SSRN converts
  Word itself); content identical.
