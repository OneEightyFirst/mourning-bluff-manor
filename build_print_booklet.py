"""Builds a print-ready, saddle-stitch booklet: core rules + full cast dossiers.

Pipeline:
  1. Render rules/core-rules.md and every cast/*.md file (full text, not a
     summary) onto "digest" half-letter pages (5.5 x 8.5 in, portrait),
     reusing build_booklet.py's Markdown renderer so typography matches the
     main rulebook.
  2. Pad the page count up to a multiple of 4 (a saddle-stitch requirement:
     every physical sheet holds 4 logical pages).
  3. Impose those pages 2-up onto landscape Letter sheets (11 x 8.5 in) in
     the standard front/back saddle-stitch order, so that printing this PDF
     duplex in landscape, then folding the stack at the center and stapling
     the fold, produces correctly-ordered reading pages.

Print instructions (also echoed by build()):
  - Paper: Letter, orientation Landscape, scale: Actual size / 100% (no
    "fit to page").
  - Duplex: on, "Flip on Short Edge." If the backs come out upside-down
    relative to the fronts, reprint with "Flip on Long Edge" instead;
    booklet-fold duplex conventions vary by printer/driver. Test with the
    first sheet (this PDF's pages 1-2) before running the full job.
  - Fold each printed sheet in half (bringing the left edge to the right
    edge) and nest the sheets in order; staple through the center fold.

If the rulebook and this booklet ever disagree, rules/core-rules.md and
cast/*.md are correct, regenerate this file.
"""

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph,
)
from pypdf import PdfReader, PdfWriter, PageObject

import build_booklet as bb

# This print booklet is black-and-white only, no parchment background fill,
# no rust/muted color accents, to keep home-printer ink/toner cost down.
# Overriding these module-level colors on the imported build_booklet module
# affects every style and table it builds for us (styles(), render_markdown())
# without touching build_booklet.py's own separately-run, full-color output.
bb.PAPER = colors.white
bb.INK = colors.black
bb.RUST = colors.black
bb.MUTED = colors.black
bb.RULE = colors.black
bb.PANEL = colors.white

ROOT = Path(__file__).resolve().parent
CONTENT_PDF = ROOT / "output" / "pdf" / "_print-booklet-content.pdf"
OUTPUT = ROOT / "output" / "pdf" / "mourning-bluff-manor-print-booklet.pdf"
COVER_IMAGE = ROOT / "assets" / "covers" / "mourning-bluff-manor-cover-door-white.png"

HALF_W, HALF_H = 5.5 * inch, 8.5 * inch  # digest page, portrait
SHEET_W, SHEET_H = 11 * inch, 8.5 * inch  # landscape Letter


def draw_digest_page(canvas, doc):
    # Plain white page, no background fill. Just a thin black rule and a
    # page number, kept deliberately light on ink.
    canvas.saveState()
    canvas.setStrokeColor(colors.black)
    canvas.setLineWidth(0.5)
    canvas.line(0.55 * inch, 0.32 * inch, HALF_W - 0.55 * inch, 0.32 * inch)
    canvas.setFont("Helvetica", 6.4)
    canvas.setFillColor(colors.black)
    canvas.drawCentredString(HALF_W / 2, 0.16 * inch, str(doc.page))
    canvas.restoreState()


def keep_sections_together(story):
    """Group each heading with every flowable up to (but not including) the
    next heading, and wrap each group in KeepTogether. This makes page
    breaks prefer landing between headings rather than mid-paragraph or
    mid-list. A group that's too tall to fit on an empty page falls back to
    reportlab's normal flowing/splitting for that group only, so a long
    section (e.g. all of Core Rules) still spans pages without erroring."""
    result = []
    i, n = 0, len(story)
    while i < n:
        item = story[i]
        is_heading = isinstance(item, Paragraph) and getattr(item.style, "name", None) in bb.HEADING_STYLE_NAMES
        if not is_heading:
            result.append(item)
            i += 1
            continue
        group = [item]
        j = i + 1
        while j < n:
            nxt = story[j]
            if isinstance(nxt, PageBreak):
                break
            if isinstance(nxt, Paragraph) and getattr(nxt.style, "name", None) in bb.HEADING_STYLE_NAMES:
                break
            group.append(nxt)
            j += 1
        result.append(KeepTogether(group))
        i = j
    return result


def build_content_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(CONTENT_PDF),
        pagesize=(HALF_W, HALF_H),
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.55 * inch,
        title="Mourning Bluff Manor: Print Booklet",
        author="Michael Wells",
        subject="Core rules and full Cast dossiers, saddle-stitch layout",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    # Full-bleed frame for the cover only: no margins, no footer/rule/page
    # number drawn (onPage=None), so the cover art fills the entire page
    # edge to edge with nothing else on it.
    cover_frame = Frame(0, 0, HALF_W, HALF_H, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    # "cover" is listed first so it's the default template for page 1;
    # NextPageTemplate("digest") below switches every page after that.
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=[cover_frame], onPage=lambda c, d: None),
        PageTemplate(id="digest", frames=[frame], onPage=draw_digest_page),
    ])
    s = bb.styles(doc.width)

    story = []

    # Cover: the door illustration, full-bleed, no caption or footer.
    # Fit within the page preserving aspect ratio (no stretching); any
    # leftover margin is invisible since the page and image are both
    # actual white.
    cover_reader = ImageReader(str(COVER_IMAGE))
    img_w, img_h = cover_reader.getSize()
    img_ratio = img_w / img_h
    if HALF_H * img_ratio <= HALF_W:
        draw_h, draw_w = HALF_H, HALF_H * img_ratio
    else:
        draw_w, draw_h = HALF_W, HALF_W / img_ratio
    cover_image = Image(str(COVER_IMAGE), width=draw_w, height=draw_h)
    cover_image.hAlign = "CENTER"
    story.append(cover_image)
    # NextPageTemplate must be queued BEFORE the PageBreak that triggers the
    # transition, not after: the pending template is consumed by the page
    # break itself, so putting it after left page 2 still on the cover's
    # zero-margin, no-footer template for one extra page.
    story.append(NextPageTemplate("digest"))
    story.append(PageBreak())

    # Core rules
    core_rules_text = (ROOT / "rules" / "core-rules.md").read_text(encoding="utf-8")
    story.extend(bb.render_markdown(core_rules_text, s))
    story.append(PageBreak())

    # Full cast dossiers, in the same order as the main booklet's roster.
    # cast/*.md headings mix "## Weakness — Name" (em-dash) and
    # "## Weakness: Name" (colon) styles; bb.clean() turns em-dashes into
    # ", " for prose, which reads fine mid-sentence but garbles a heading
    # into "Weakness , Name". Normalize both to a colon here, for this
    # rendering only, the source files themselves are left untouched.
    heading_pattern = re.compile(r"^## (Weakness|Gift|Tool)\s*[—:-]\s*(.+)$", re.MULTILINE)
    for index, filename in enumerate(bb.CAST_FILES):
        cast_text = (ROOT / "cast" / filename).read_text(encoding="utf-8")
        cast_text = heading_pattern.sub(r"## \1: \2", cast_text)
        story.extend(bb.render_markdown(cast_text, s))
        if index < len(bb.CAST_FILES) - 1:
            story.append(PageBreak())

    doc.build(keep_sections_together(story))
    return CONTENT_PDF


def pad_to_multiple_of_4(reader):
    """Pad up to a multiple of 4 with plain blank (white, unfilled) pages,
    matching every real content page now that there's no background tint."""
    pages = list(reader.pages)
    remainder = len(pages) % 4
    if remainder:
        blanks_needed = 4 - remainder
        for _ in range(blanks_needed):
            pages.append(PageObject.create_blank_page(width=HALF_W, height=HALF_H))
    return pages


def impose_booklet(pages):
    """2-up saddle-stitch imposition. pages is 0-indexed; formulas below are
    written in 1-indexed logical-page terms per the standard booklet-print
    algorithm, then converted back to 0-indexed list access."""
    total = len(pages)
    sheets = total // 4
    writer = PdfWriter()

    def get(logical_1_indexed):
        return pages[logical_1_indexed - 1]

    def blank_sheet():
        return PageObject.create_blank_page(width=SHEET_W, height=SHEET_H)

    def place(sheet_page, left_src, right_src):
        sheet_page.merge_translated_page(left_src, 0, 0, expand=False)
        sheet_page.merge_translated_page(right_src, HALF_W, 0, expand=False)

    for s in range(1, sheets + 1):
        fl = total - 2 * (s - 1)
        fr = 2 * (s - 1) + 1
        bl = 2 * (s - 1) + 2
        br = total - (2 * (s - 1) + 1)

        front = blank_sheet()
        place(front, get(fl), get(fr))
        writer.add_page(front)

        back = blank_sheet()
        place(back, get(bl), get(br))
        writer.add_page(back)

    return writer


def build():
    build_content_pdf()
    reader = PdfReader(str(CONTENT_PDF))
    pages = pad_to_multiple_of_4(reader)
    writer = impose_booklet(pages)
    writer.write(str(OUTPUT))

    logical_pages = len(pages)
    sheets = logical_pages // 4
    print(f"Content pages: {len(reader.pages)} (padded to {logical_pages})")
    print(f"Imposed sheets: {sheets} (physical pieces of paper)")
    print(f"Wrote {OUTPUT}")
    print()
    print("Print instructions:")
    print("  - Letter paper, Landscape orientation, Actual size / 100% scale (no fit-to-page).")
    print("  - Duplex on, 'Flip on Short Edge.' Test the first sheet (PDF pages 1-2); if the")
    print("    back prints upside-down relative to the front, use 'Flip on Long Edge' instead.")
    print("  - Fold each sheet in half (left edge to right edge) and nest sheets in order,")
    print("    then staple through the center fold.")
    return OUTPUT


if __name__ == "__main__":
    build()
