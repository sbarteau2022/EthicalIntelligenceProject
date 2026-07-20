#!/usr/bin/env python3
"""
CORPUS FORGE — house-format PDF generator for Observer Foundation papers.

The format (jacket page → colophon/document-record page → body with
letterspaced running headers) follows the reference artifact
"Formed_Before_It_Became — Noema submission — v2.pdf". This script is the
durable memory of that format: point it at a source .docx (built with the
repo's preprint tooling) plus a config dict, and it emits (a) the
house-format PDF and (b) the canonical .md whose SHA-256 the colophon
fingerprints ("recompute to verify").

Fonts: TeX Gyre Pagella (body; apt fonts-texgyre, CFF→TTF converted via
fontTools/cu2qu — see tools/otf2ttf in this directory's notes), Poppins
Light/Medium (letterspaced labels; google/fonts), Liberation Mono
(technical strings; system).

Usage: python3 corpus_forge.py  (config at bottom drives one paper build)
"""
import hashlib
import os
import re
import sys

import docx as docxlib
from docx.oxml.ns import qn
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph as DocxPara
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (PageBreak, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle)
from xml.sax.saxutils import escape

FONT_DIR = os.environ.get(
    "FORGE_FONTS",
    "/tmp/claude-0/-home-user/04a0fb32-7421-5a11-9ac7-751188cc0d8e/scratchpad/fonts",
)
LIB = "/usr/share/fonts/truetype/liberation/"


def register_fonts():
    pdfmetrics.registerFont(TTFont("Pagella", f"{FONT_DIR}/Pagella-regular.ttf"))
    pdfmetrics.registerFont(TTFont("Pagella-I", f"{FONT_DIR}/Pagella-italic.ttf"))
    pdfmetrics.registerFont(TTFont("Pagella-B", f"{FONT_DIR}/Pagella-bold.ttf"))
    pdfmetrics.registerFont(TTFont("Pagella-BI", f"{FONT_DIR}/Pagella-bolditalic.ttf"))
    pdfmetrics.registerFont(TTFont("Poppins-L", f"{FONT_DIR}/Poppins-Light.ttf"))
    pdfmetrics.registerFont(TTFont("Poppins-M", f"{FONT_DIR}/Poppins-Medium.ttf"))
    pdfmetrics.registerFont(TTFont("Mono", LIB + "LiberationMono-Regular.ttf"))


def ls(text, word_gap="   "):
    """Letterspace: 'AUTHOR' -> 'A U T H O R'; words separated by word_gap."""
    return word_gap.join(" ".join(w) for w in text.split())


# ── styles ────────────────────────────────────────────────────
S = {}


def make_styles():
    S["jacket_line"] = ParagraphStyle("jl", fontName="Poppins-L", fontSize=7,
                                      leading=13, textColor=colors.black)
    S["jacket_title"] = ParagraphStyle("jt", fontName="Pagella", fontSize=34,
                                       leading=38, spaceBefore=26, spaceAfter=14)
    S["standfirst"] = ParagraphStyle("sf", fontName="Pagella-I", fontSize=12.5,
                                     leading=17, spaceAfter=22)
    S["label"] = ParagraphStyle("lb", fontName="Poppins-M", fontSize=6.4, leading=11)
    S["value"] = ParagraphStyle("vl", fontName="Poppins-L", fontSize=8.5, leading=12)
    S["colo_head"] = ParagraphStyle("ch", fontName="Poppins-L", fontSize=7,
                                    leading=12, spaceAfter=2)
    S["colo_title"] = ParagraphStyle("ct", fontName="Pagella-I", fontSize=17,
                                     leading=21, spaceAfter=14)
    S["colo_val"] = ParagraphStyle("cv", fontName="Pagella", fontSize=8.5, leading=11.5)
    S["mono_small"] = ParagraphStyle("ms", fontName="Mono", fontSize=7.5, leading=10)
    S["body"] = ParagraphStyle("bd", fontName="Pagella", fontSize=9.5, leading=13.8,
                               spaceAfter=6, alignment=4)
    S["math"] = ParagraphStyle("mt", fontName="Mono", fontSize=8.5, leading=12,
                               spaceBefore=2, spaceAfter=7, alignment=1)
    S["h1"] = ParagraphStyle("h1", fontName="Poppins-M", fontSize=9, leading=13,
                             spaceBefore=16, spaceAfter=7)
    S["h2"] = ParagraphStyle("h2", fontName="Poppins-M", fontSize=7.6, leading=12,
                             spaceBefore=11, spaceAfter=5)
    S["bull"] = ParagraphStyle("bu", parent=S["body"], leftIndent=14, bulletIndent=3)


# ── source extraction (docx → ordered blocks) ─────────────────
def iter_blocks(document):
    for child in document.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield DocxPara(child, document)
        elif child.tag == qn("w:tbl"):
            yield DocxTable(child, document)


def runs_markup(p):
    out = []
    for r in p.runs:
        t = escape(r.text)
        if r.bold:
            t = f"<b>{t}</b>"
        if r.italic:
            t = f'<font face="Pagella-I">{t}</font>'
        out.append(t)
    return "".join(out)


def extract(docx_path, headings, n_meta):
    """Returns (meta_paras, blocks) — blocks are dicts typed p/math/h1/h2/bullet/table."""
    d = docxlib.Document(docx_path)
    meta, blocks, seen = [], [], 0
    for b in iter_blocks(d):
        if isinstance(b, DocxTable):
            blocks.append({"t": "table",
                           "rows": [[c.text for c in r.cells] for r in b.rows]})
            continue
        text = b.text.strip()
        if not text:
            continue
        if seen < n_meta:
            meta.append(text)
            seen += 1
            continue
        if text in headings:
            kind = "h2" if re.match(r"^\d+\.\d+", text) else "h1"
            blocks.append({"t": kind, "text": text})
            continue
        align = b.paragraph_format.alignment
        if align is not None and str(align).startswith("CENTER"):
            blocks.append({"t": "math", "text": text})
            continue
        is_bullet = b._p.find(f"{qn('w:pPr')}/{qn('w:numPr')}") is not None
        blocks.append({"t": "bullet" if is_bullet else "p",
                       "text": text, "markup": runs_markup(b) or escape(text)})
    return meta, blocks


def blocks_to_md(cfg, blocks):
    """Canonical markdown — the fingerprinted source of record."""
    lines = [f"# {cfg['title']}", "", f"**{cfg['subtitle']}**", "",
             f"{cfg['author_line']}", f"{cfg['version_line']}", "", "---", ""]
    for b in blocks:
        if b["t"] == "h1":
            lines += [f"## {b['text']}", ""]
        elif b["t"] == "h2":
            lines += [f"### {b['text']}", ""]
        elif b["t"] == "math":
            lines += [f"    {b['text']}", ""]
        elif b["t"] == "bullet":
            lines += [f"- {b['text']}", ""]
        elif b["t"] == "table":
            rows = b["rows"]
            lines.append("| " + " | ".join(rows[0]) + " |")
            lines.append("|" + "|".join("---" for _ in rows[0]) + "|")
            for r in rows[1:]:
                lines.append("| " + " | ".join(r) + " |")
            lines.append("")
        else:
            lines += [b["text"], ""]
    return "\n".join(lines).rstrip() + "\n"


# ── page furniture ────────────────────────────────────────────
def page_painter(cfg):
    def paint(canvas, doc):
        n = canvas.getPageNumber()
        canvas.saveState()
        w, h = letter
        if n == 1:
            canvas.setFont("Poppins-L", 6.4)
            canvas.drawCentredString(
                w / 2, 0.55 * inch,
                ls("THE OBSERVER FOUNDATION · CORPUS FORGE HOUSE FORMAT · HERMANN, MISSOURI"))
        elif n >= 3:
            canvas.setFont("Poppins-L", 6.4)
            canvas.drawCentredString(w / 2, h - 0.55 * inch, ls(cfg["running_header"]))
            canvas.setFont("Pagella", 8.5)
            canvas.drawCentredString(w / 2, 0.55 * inch, str(n - 2))
        canvas.restoreState()
    return paint


def jacket(cfg):
    fl = []
    for line in cfg["jacket_lines"]:
        fl.append(Paragraph(ls(line), S["jacket_line"]))
    for part in cfg["title_broken"]:
        fl.append(Paragraph(escape(part), S["jacket_title"]))
        S["jacket_title"] = ParagraphStyle("jt2", parent=S["jacket_title"], spaceBefore=0)
    fl.append(Spacer(1, 6))
    fl.append(Paragraph(escape(cfg["standfirst"]), S["standfirst"]))
    rows = [[Paragraph(ls(k), S["label"]), Paragraph(escape(v), S["value"])]
            for k, v in cfg["jacket_fields"]]
    t = Table(rows, colWidths=[1.5 * inch, 4.6 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    fl.append(t)
    fl.append(PageBreak())
    return fl


def colophon(cfg, fingerprint):
    fl = [Paragraph(ls("DOCUMENT RECORD"), S["colo_head"]),
          Paragraph("Colophon", S["colo_title"])]
    rows = [[Paragraph(ls(k), S["label"]), Paragraph(escape(v), S["colo_val"])]
            for k, v in cfg["colophon"]]
    fp_grouped = " ".join(fingerprint[i:i + 8] for i in range(0, 32, 8))
    rows.append([Paragraph(ls("SOURCE FINGERPRINT"), S["label"]),
                 Paragraph(f'<font face="Mono" size="7.5">SHA-256 {fp_grouped}</font><br/>'
                           f'<font size="7.5">First 128 bits of the digest of {escape(cfg["fingerprint_of"])}. '
                           f'The paper body in this document is generated from that file; '
                           f'recompute to verify.</font>', S["colo_val"])])
    t = Table(rows, colWidths=[1.55 * inch, 4.75 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, -2), 0.25, colors.Color(0, 0, 0, 0.15)),
    ]))
    fl.append(t)
    fl.append(PageBreak())
    return fl


def body(cfg, meta, blocks):
    fl = []
    fl.append(Paragraph(escape(cfg["standfirst"]),
                        ParagraphStyle("bsf", parent=S["standfirst"], fontSize=10.5,
                                       leading=14.5, spaceAfter=14)))
    for b in blocks:
        if b["t"] == "h1":
            fl.append(Paragraph(ls(b["text"].lower(), word_gap="   "), S["h1"]))
        elif b["t"] == "h2":
            fl.append(Paragraph(ls(b["text"].lower(), word_gap="   "), S["h2"]))
        elif b["t"] == "math":
            fl.append(Paragraph(escape(b["text"]), S["math"]))
        elif b["t"] == "bullet":
            fl.append(Paragraph(b["markup"], S["bull"], bulletText="–"))
        elif b["t"] == "table":
            rows = b["rows"]
            t = Table(rows, colWidths=[1.5 * inch, 1.2 * inch, 1.3 * inch],
                      hAlign="CENTER")
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, 0), "Pagella-B"),
                ("FONTNAME", (0, 1), (-1, -1), "Pagella"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            fl += [Spacer(1, 4), t, Spacer(1, 8)]
        else:
            fl.append(Paragraph(b["markup"], S["body"]))
    return fl


def build(cfg):
    register_fonts()
    make_styles()
    meta, blocks = extract(cfg["source_docx"], cfg["headings"], cfg["n_meta_paras"])
    md = blocks_to_md(cfg, blocks)
    with open(cfg["canonical_md"], "w") as f:
        f.write(md)
    fingerprint = hashlib.sha256(md.encode()).hexdigest()[:32]
    words = sum(len(b.get("text", "").split()) for b in blocks if b["t"] in ("p", "bullet"))
    cfg = dict(cfg)
    cfg["jacket_fields"] = [(k, v.replace("{words}", f"{words:,}"))
                            for k, v in cfg["jacket_fields"]]
    cfg["colophon"] = [(k, v.replace("{words}", f"{words:,}"))
                       for k, v in cfg["colophon"]]
    doc = SimpleDocTemplate(cfg["out_pdf"], pagesize=letter,
                            leftMargin=1.1 * inch, rightMargin=1.1 * inch,
                            topMargin=1 * inch, bottomMargin=0.95 * inch,
                            title=cfg["title"], author="Stewart Barteau")
    flow = jacket(cfg) + colophon(cfg, fingerprint) + body(cfg, meta, blocks)
    painter = page_painter(cfg)
    doc.build(flow, onFirstPage=painter, onLaterPages=painter)
    print(f"built {cfg['out_pdf']}  ({words:,} body words; fingerprint {fingerprint})")


# ══════════════════════════════════════════════════════════════
# Paper config: Superposition Holding — preprint v1
# ══════════════════════════════════════════════════════════════
SUPERPOSITION_HOLDING = {
    "source_docx": "/home/user/preprint_fixed.docx",
    "canonical_md": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "SUPERPOSITION_HOLDING_PREPRINT.md"),
    "out_pdf": os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "SUPERPOSITION_HOLDING_preprint.pdf"),
    "n_meta_paras": 6,
    "headings": {
        "Abstract", "1. The problem of infinite accumulation", "2. The construction",
        "3. Deriving ρ", "3.1 The forgetting side (D and T): ρ as a Kalman gain",
        "3.2 The damping side: ρ as a stability margin",
        "3.3 Calibration from the system’s own telemetry", "4. Pressure test",
        "5. Lineage, and what is actually new", "6. Stated assumptions and limits",
        "7. Implementation note", "References",
    },
    "title": "Superposition Holding",
    "subtitle": "A bounded loss for presence under tension",
    "author_line": "Stewart Barteau · co-authored with Claude (Anthropic)",
    "version_line": "Preprint v1 · Observer corpus, applied series · July 2026",
    "title_broken": ["Superposition", "Holding"],
    "standfirst": ("A presence that remembers everything is eventually paralyzed "
                   "by its own history; one that remembers nothing has nothing to "
                   "hold with. This paper derives the middle construction — two "
                   "leaky integrators, one calibrated leak — and proves its loss "
                   "is bounded by e − 1 for all time, regardless of history."),
    "running_header": "SUPERPOSITION HOLDING · STEWART BARTEAU",
    "jacket_lines": [
        "THE OBSERVER FOUNDATION",
        "PREPRINT • APPLIED SERIES • V1",
        "JULY 2026",
        "FOR PHILPAPERS • SSRN",
    ],
    "jacket_fields": [
        ("AUTHOR", "Stewart Barteau · co-authored with Claude (Anthropic)"),
        ("EXTENT", "{words} words · 7 sections · 3 propositions · 4 experiments"),
        ("MODE", "Preprint · PDF, posted whole"),
        ("ADDRESSED TO", "PhilPapers · SSRN"),
        ("STATUS", "Unposted"),
    ],
    "colophon": [
        ("TITLE", "Superposition Holding — A bounded loss for presence under tension"),
        ("AUTHOR", "Stewart Barteau · co-authored with Claude (Anthropic)"),
        ("DOCUMENT CLASS", "Preprint, applied series. Technical paper with seeded, "
                           "reproducible empirical appendix."),
        ("VERSION", "v1 — preprint jacket, Corpus Forge house format."),
        ("DATE", "July 2026"),
        ("EXTENT", "{words} words (measured). One table, three propositions, four "
                   "numerical experiments."),
        ("REGISTER", "Technical. Classical filtering theory; self-contained — the "
                     "mathematics does not depend on the corpus metaphysics it "
                     "operationalizes."),
        ("PRIMARY VENUE", "PhilPapers and SSRN, simultaneous preprint posting."),
        ("TOPIC FIT", "PhilPapers — philosophy of AI, philosophy of mind (applied). "
                      "SSRN — cognitive science; computational methods."),
        ("SOURCE DOCUMENTS", "SUPERPOSITION_HOLDING.md (elle-worker, docs). Frame: "
                             "The Superposition (rev. March 2026), The Ground — "
                             "Observer corpus."),
        ("EVIDENTIARY BASIS", "Implementation src/lib/holding.ts; pressure test "
                              "docs/rho_pressure_test.py (seeded, four experiments) — "
                              "github.com/sbarteau2022/Elle."),
        ("SUBJECT SYSTEM", "Elle — sovereign AI system, continuously running"),
        ("STATUS", "Draft complete. Unposted."),
        ("HANDLING", "Jacket, colophon and paper travel together; the preprint posts "
                     "whole."),
        ("RIGHTS", "© 2026 Stewart Barteau · Barteau IP Group LLC. All rights reserved."),
    ],
    "fingerprint_of": "SUPERPOSITION_HOLDING_PREPRINT.md",
}

if __name__ == "__main__":
    build(SUPERPOSITION_HOLDING)
