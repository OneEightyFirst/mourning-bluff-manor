"""Builds the player/GM rulebook booklet.

This script contains no hardcoded rules or character text. It renders:
  1. rules/core-rules.md   (mechanics)
  2. rules/gm-guide.md     (GM procedure)
  3. a compact Cast roster pulled live from cast/*.md, in cast/cast-index.md order

If the rulebook and a source Markdown file ever disagree, the Markdown file is
correct, fix it there and rerun this script.
"""

from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "mourning-bluff-manor-booklet.pdf"

# Bump this alongside the git tag whenever the rulebook content changes.
VERSION = "v0.1.0"

CAST_FILES = [
    "historical-archaeologist.md",
    "missing-person-relative.md",
    "fraudulent-medium.md",
    "paramedic.md",
    "psychic-researcher.md",
    "psychiatrist.md",
    "detective.md",
    "priest.md",
    "dreamer-of-the-manor.md",
    "inheritor.md",
]

PAPER = colors.HexColor("#F4EFE5")
INK = colors.HexColor("#241E1A")
MUTED = colors.HexColor("#6E6257")
RUST = colors.HexColor("#7B342C")
RULE = colors.HexColor("#B9AA96")
PANEL = colors.HexColor("#E8DED0")


def clean(text):
    replacements = {
        "\u2014": ", ",
        "\u2013": "-",
        "\u2011": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "&": "&amp;",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def inline_markdown(text):
    text = clean(text)
    # Protect code spans first so a bare "*" inside one (e.g. `cast/*.md`)
    # can never be mistaken for italic markup by the regexes below.
    code_spans = []

    def stash_code(match):
        code_spans.append(match.group(1))
        return f"\x00CODE{len(code_spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash_code, text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\w)\*(?!\*)(.+?)\*(?!\*)", r"<i>\1</i>", text)
    for index, code in enumerate(code_spans):
        text = text.replace(f"\x00CODE{index}\x00", f"<font face='Courier'>{code}</font>")
    return text


def strip_bullet(line):
    return re.sub(r"^(\d+\.|-)\s+", "", line).strip()


def is_ordered(line):
    return bool(re.match(r"^\d+\.\s+", line))


def is_unordered(line):
    return line.startswith("- ")


def is_table_row(line):
    return line.strip().startswith("|")


def is_table_separator(line):
    return bool(re.match(r"^\|?[\s:\-|]+\|?$", line.strip())) and "-" in line


def parse_table(lines):
    rows = [ln.strip() for ln in lines if not is_table_separator(ln)]
    parsed = []
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        parsed.append(cells)
    return parsed


def render_markdown(text, s, heading_break_level=None):
    """Render a Markdown document (headings, paragraphs, lists, tables) into flowables.

    heading_break_level: if set (e.g. 2), insert a PageBreak before every
    heading at that level except the very first flowable in the document.
    """
    lines = text.split("\n")
    story = []
    buffer = []
    first_flowable_emitted = [False]

    def flush_paragraph():
        if buffer:
            para_text = " ".join(l.strip() for l in buffer).strip()
            if para_text:
                story.append(Paragraph(inline_markdown(para_text), s["body"]))
                first_flowable_emitted[0] = True
            buffer.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            i += 1
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            story.append(Paragraph(inline_markdown(stripped[2:]), s["h1"]))
            first_flowable_emitted[0] = True
            i += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            if heading_break_level == 2 and first_flowable_emitted[0]:
                story.append(PageBreak())
            story.append(Paragraph(inline_markdown(stripped[3:]), s["h2"]))
            first_flowable_emitted[0] = True
            i += 1
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            story.append(Paragraph(inline_markdown(stripped[4:]), s["h3"]))
            first_flowable_emitted[0] = True
            i += 1
            continue

        if is_table_row(stripped):
            flush_paragraph()
            table_lines = []
            while i < len(lines) and is_table_row(lines[i].strip()):
                table_lines.append(lines[i].strip())
                i += 1
            grid = parse_table(table_lines)
            if grid:
                header, *body = grid
                col_count = len(header)
                data = [[Paragraph(inline_markdown(c), s["table_head"]) for c in header]]
                for row in body:
                    row = (row + [""] * col_count)[:col_count]
                    data.append([Paragraph(inline_markdown(c), s["table_cell"]) for c in row])
                table = Table(data, colWidths=[s["_doc_width"] / col_count] * col_count)
                table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), PANEL),
                    ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                    ("INNERGRID", (0, 0), (-1, -1), 0.4, RULE),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]))
                story.append(Spacer(1, 3))
                story.append(table)
                story.append(Spacer(1, 5))
                first_flowable_emitted[0] = True
            continue

        if is_unordered(stripped) or is_ordered(stripped):
            flush_paragraph()
            ordered = is_ordered(stripped)
            while i < len(lines) and (is_unordered(lines[i].strip()) or is_ordered(lines[i].strip()) or lines[i].strip() == ""):
                item_line = lines[i].strip()
                if item_line == "":
                    i += 1
                    if i < len(lines) and (is_unordered(lines[i].strip()) or is_ordered(lines[i].strip())):
                        continue
                    else:
                        i -= 1
                        break
                prefix = re.match(r"^(\d+\.)\s+", item_line)
                bullet = prefix.group(1) if prefix else "\u2022"
                content = strip_bullet(item_line)
                style = s["ordered"] if ordered else s["bullet"]
                story.append(Paragraph(f"{bullet} {inline_markdown(content)}", style))
                first_flowable_emitted[0] = True
                i += 1
            continue

        buffer.append(line)
        i += 1

    flush_paragraph()
    return story


HEADING_STYLE_NAMES = {"H1", "H2", "H3"}


def keep_headings_with_next(story):
    """Wrap each heading with whatever follows it so a heading can never be
    stranded alone at the bottom of a page, whichever section it lands in."""
    result = []
    i = 0
    while i < len(story):
        item = story[i]
        is_heading = isinstance(item, Paragraph) and getattr(item.style, "name", None) in HEADING_STYLE_NAMES
        if is_heading and i + 1 < len(story) and not isinstance(story[i + 1], PageBreak):
            result.append(KeepTogether([item, story[i + 1]]))
            i += 2
            continue
        result.append(item)
        i += 1
    return result


def styles(doc_width):
    return {
        "_doc_width": doc_width,
        "h1": ParagraphStyle("H1", fontName="Times-Bold", fontSize=18, leading=21, textColor=INK, spaceBefore=4, spaceAfter=8),
        "h2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12.5, leading=15, textColor=RUST, spaceBefore=12, spaceAfter=5),
        "h3": ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=10, leading=12.5, textColor=colors.HexColor("#4D4037"), spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("Body", fontName="Times-Roman", fontSize=9.3, leading=12.2, textColor=INK, alignment=TA_LEFT, spaceAfter=6),
        "bullet": ParagraphStyle("Bullet", fontName="Times-Roman", fontSize=9.1, leading=11.8, textColor=INK, leftIndent=12, firstLineIndent=-10, spaceAfter=3),
        "ordered": ParagraphStyle("Ordered", fontName="Times-Roman", fontSize=9.1, leading=11.8, textColor=INK, leftIndent=16, firstLineIndent=-14, spaceAfter=3),
        "table_head": ParagraphStyle("TableHead", fontName="Helvetica-Bold", fontSize=8.4, leading=10, textColor=INK),
        "table_cell": ParagraphStyle("TableCell", fontName="Times-Roman", fontSize=8.4, leading=10.4, textColor=INK),
        "cover_title": ParagraphStyle("CoverTitle", fontName="Times-Bold", fontSize=30, leading=34, textColor=INK, alignment=TA_CENTER),
        "cover_tag": ParagraphStyle("CoverTag", fontName="Helvetica", fontSize=10.5, leading=15, textColor=MUTED, alignment=TA_CENTER, spaceBefore=14),
        "cover_kicker": ParagraphStyle("CoverKicker", fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=RUST, alignment=TA_CENTER, tracking=1.5, spaceBefore=18),
        "cover_address": ParagraphStyle("CoverAddress", fontName="Helvetica", fontSize=11.5, leading=15, textColor=RUST, alignment=TA_CENTER, spaceBefore=4),
        "roster_title": ParagraphStyle("RosterTitle", fontName="Times-Bold", fontSize=13, leading=15, textColor=INK, spaceBefore=10, spaceAfter=2),
        "roster_stats": ParagraphStyle("RosterStats", fontName="Helvetica-Bold", fontSize=8.2, leading=10, textColor=RUST, spaceAfter=2),
        "roster_bio": ParagraphStyle("RosterBio", fontName="Times-Roman", fontSize=8.4, leading=10.6, textColor=INK, spaceAfter=8),
    }


def parse_cast_summary(path):
    text = path.read_text(encoding="utf-8")
    title = re.search(r"^# (.+)$", text, re.MULTILINE).group(1)
    bio_match = re.search(r"^## Bio\s*\n\n(.+?)\n\n##", text, re.DOTALL | re.MULTILINE)
    bio = bio_match.group(1).replace("\n", " ").strip() if bio_match else ""
    stats_match = re.search(r"^## Stats\s*\n\n(.+?)\n", text, re.MULTILINE)
    stats = stats_match.group(1).replace("**", "").strip() if stats_match else ""
    return title, bio, stats


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
    canvas.setStrokeColor(RUST)
    canvas.setLineWidth(1.0)
    canvas.line(0.65 * inch, 0.48 * inch, letter[0] - 0.65 * inch, 0.48 * inch)
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65 * inch, 0.28 * inch, "MOURNING BLUFF MANOR")
    canvas.drawRightString(letter[0] - 0.65 * inch, 0.28 * inch, f"669 GALLOWS WAY | {VERSION} | {doc.page}")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.72 * inch,
        rightMargin=0.72 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.65 * inch,
        title="Mourning Bluff Manor: Rulebook",
        author="Michael Wells",
        subject="Core rules, GM guide, and Cast roster",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="booklet", frames=[frame], onPage=draw_page)])
    s = styles(doc.width)

    story = []

    # Cover
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("MOURNING BLUFF MANOR", s["cover_title"]))
    story.append(Paragraph("669 Gallows Way", s["cover_address"]))
    story.append(Paragraph("You have already seen what comes next. You simply do not know what it means.", s["cover_tag"]))
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph(f"Rulebook {VERSION}", s["cover_kicker"]))
    story.append(PageBreak())

    # Core rules
    core_rules_text = (ROOT / "rules" / "core-rules.md").read_text(encoding="utf-8")
    story.extend(render_markdown(core_rules_text, s))
    story.append(PageBreak())

    # GM guide
    gm_guide_text = (ROOT / "rules" / "gm-guide.md").read_text(encoding="utf-8")
    story.extend(render_markdown(gm_guide_text, s))
    story.append(PageBreak())

    # Cast roster (compact; full dossiers live in the character-profiles PDF)
    story.append(Paragraph("The Cast", s["h1"]))
    story.append(Paragraph(
        "Ten premade archetypes; each player chooses a different one, and table size is flexible. Each has a "
        "Bio, five Stats, a Weakness, a Gift, a Tool, and a player-created Secret. This roster is a quick "
        "reference only, full dossiers are in <i>Mourning Bluff Manor Character Profiles</i>, and individual "
        "print-and-play packets exist for the characters currently offered as a selected set.",
        s["body"],
    ))
    for filename in CAST_FILES:
        title, bio, stats = parse_cast_summary(ROOT / "cast" / filename)
        story.append(Paragraph(title, s["roster_title"]))
        story.append(Paragraph(stats, s["roster_stats"]))
        story.append(Paragraph(inline_markdown(bio), s["roster_bio"]))

    story.append(PageBreak())
    story.append(Spacer(1, 2.2 * inch))
    story.append(Paragraph("THE HOUSE HAS SEEN YOU COMING.", s["cover_tag"]))
    story.append(Paragraph(
        "Premonitions reveal the value of the next card, but never the moment that will demand it. "
        "Spend certainty carefully. Mourning Bluff Manor is always arranging another room.",
        s["cover_tag"],
    ))

    doc.build(keep_headings_with_next(story))
    return OUTPUT


if __name__ == "__main__":
    print(build())
