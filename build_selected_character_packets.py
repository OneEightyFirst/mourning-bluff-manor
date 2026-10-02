"""Builds individual print-and-play character packets.

Every piece of character-specific text (Bio, What Is Established, Make the
Character Your Own, Decide Before Play, Stats, Weakness, Gift, Tool, Secret)
is parsed live from the corresponding file in cast/. This script contains no
hardcoded character text; add a character to SELECTED below and write its
"What Is Established" / "Make the Character Your Own" / "Decide Before Play"
sections in its cast/*.md file, that's the only source of truth.
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
    TopPadder,
)


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "output" / "pdf" / "selected-characters"

PAPER = colors.white
INK = colors.black
MUTED = colors.HexColor("#555555")
RUST = colors.black
RULE = colors.HexColor("#999999")
PANEL = colors.HexColor("#EDEDED")
PALE = colors.HexColor("#F5F5F5")

# Slug -> source Markdown file in cast/. This is the only place the roster of
# "currently offered" packets is decided; everything else is parsed.
SELECTED = {
    "inheritor": "inheritor.md",
    "dreamer": "dreamer-of-the-manor.md",
    "psychic-researcher": "psychic-researcher.md",
    "paramedic": "paramedic.md",
    "detective": "detective.md",
    "fraudulent-medium": "fraudulent-medium.md",
    "historical-archaeologist": "historical-archaeologist.md",
}

REQUIRED_SECTIONS = ("What Is Established", "Make the Character Your Own", "Decide Before Play")


def clean(text):
    replacements = {
        "\u2014": " - ",
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
    if text.startswith("*") and text.endswith("*") and not text.startswith("**"):
        return f"<i>{text[1:-1]}</i>"
    return text


def strip_bullet(text):
    return re.sub(r"^-\s+", "", text.strip())


def parse_profile(path):
    text = path.read_text(encoding="utf-8")
    title = clean(re.search(r"^# (.+)$", text, re.MULTILINE).group(1))
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    sections = {}
    for index in range(1, len(parts), 2):
        heading = clean(parts[index])
        heading = re.sub(r"^(Weakness|Gift|Tool)\s*[,\u2014:-]\s*", r"\1: ", heading)
        body = clean(parts[index + 1].strip())
        sections[heading] = [p.strip() for p in body.split("\n\n") if p.strip()]
    missing = [name for name in REQUIRED_SECTIONS if name not in sections]
    if missing:
        raise ValueError(
            f"{path.name} is missing {missing}; it cannot be built as a selected-character packet "
            "until those sections are written in the Markdown source."
        )
    return title, sections


def draw_page(character_title):
    def _draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
        canvas.setFont("Helvetica", 7.2)
        canvas.setFillColor(MUTED)
        canvas.drawString(0.65 * inch, 0.28 * inch, "MOURNING BLUFF MANOR")
        canvas.drawRightString(7.85 * inch, 0.28 * inch, character_title.upper())
        canvas.restoreState()

    return _draw


def styles(compact=False):
    body_size = 8.0 if compact else 8.35
    small_size = 7.55 if compact else 7.8
    prompt_size = 7.65 if compact else 7.9
    reference_size = 6.75 if compact else 6.9
    return {
        "title": ParagraphStyle("Title", fontName="Times-Bold", fontSize=20, leading=22, textColor=INK, alignment=TA_CENTER, spaceAfter=2),
        "kicker": ParagraphStyle("Kicker", fontName="Helvetica-Bold", fontSize=6.4, leading=7.2, tracking=1.6, textColor=RUST, alignment=TA_CENTER, spaceAfter=7),
        "section": ParagraphStyle("Section", fontName="Helvetica-Bold", fontSize=8.0, leading=9.2, textColor=RUST, spaceBefore=6, spaceAfter=2),
        "body": ParagraphStyle("Body", fontName="Times-Roman", fontSize=body_size, leading=body_size + 1.7, textColor=INK, alignment=TA_LEFT, spaceAfter=3),
        "lead": ParagraphStyle("Lead", fontName="Times-Roman", fontSize=9.2, leading=11.2, textColor=INK, alignment=TA_LEFT, spaceAfter=8),
        "small": ParagraphStyle("Small", fontName="Times-Roman", fontSize=small_size, leading=small_size + 1.4, textColor=INK, alignment=TA_LEFT, spaceAfter=2),
        "prompt": ParagraphStyle("Prompt", fontName="Times-Italic", fontSize=prompt_size, leading=prompt_size + 1.5, textColor=colors.HexColor("#4D4037"), leftIndent=8, firstLineIndent=-5, spaceAfter=3),
        "stats": ParagraphStyle("Stats", fontName="Helvetica-Bold", fontSize=7.75, leading=9.2, textColor=INK, alignment=TA_CENTER),
        "quote": ParagraphStyle("Quote", fontName="Times-Italic", fontSize=7.55, leading=8.95, textColor=colors.HexColor("#4D4037"), leftIndent=0, spaceAfter=2),
        "secret": ParagraphStyle("Secret", fontName="Times-Roman", fontSize=7.65, leading=9.1, textColor=MUTED, spaceAfter=2),
        "secret_line": ParagraphStyle("SecretLine", fontName="Helvetica", fontSize=7.2, leading=9.0, textColor=RULE, spaceAfter=0),
        "reference": ParagraphStyle("Reference", fontName="Helvetica", fontSize=reference_size, leading=reference_size + 1.25, textColor=INK, spaceAfter=4),
        "stat_ref_name": ParagraphStyle("StatRefName", fontName="Helvetica-Bold", fontSize=7.0, leading=8.0, textColor=RUST, alignment=TA_CENTER, spaceAfter=3),
        "stat_ref_body": ParagraphStyle("StatRefBody", fontName="Helvetica", fontSize=6.35, leading=7.45, textColor=INK, alignment=TA_CENTER),
    }


def panel(text, width, style, background=PALE):
    table = Table([[Paragraph(text, style)]], colWidths=[width])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.65, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
    ]))
    return table


def add_heading(story, text, style):
    story.append(Paragraph(text.upper(), style))


def stack_height(flowables, width):
    """Estimate the rendered height of a vertical flowable stack."""
    total = 0
    for flowable in flowables:
        _, height = flowable.wrap(width, 10_000)
        total += flowable.getSpaceBefore() + height + flowable.getSpaceAfter()
    return total


def build_packet(slug, source_filename):
    title, sections = parse_profile(ROOT / "cast" / source_filename)
    output = OUTPUT_DIR / f"mourning-bluff-manor-{slug}.pdf"

    doc = BaseDocTemplate(
        str(output),
        pagesize=letter,
        leftMargin=0.58 * inch,
        rightMargin=0.58 * inch,
        topMargin=0.35 * inch,
        bottomMargin=0.52 * inch,
        title=f"Mourning Bluff Manor - {title}",
        author="Michael Wells",
        subject="Player character packet",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="packet", frames=[frame], onPage=draw_page(title))])
    # The Dreamer carries substantially more character-specific rules than the
    # other packets. Keep its established compact setting; use a slightly more
    # generous reading size everywhere that the content permits it.
    compact = slug == "dreamer"
    s = styles(compact=compact)
    stats = sections["Stats"][0].replace("**", "")

    opening = f"You are <b>{title}</b>. " + " ".join(sections["Bio"])
    fixed = " ".join(sections["What Is Established"])
    custom = " ".join(sections["Make the Character Your Own"])
    questions = [strip_bullet(q) for q in sections["Decide Before Play"]]

    story = [
        Paragraph(title, s["title"]),
        panel(stats, doc.width, s["stats"], PANEL),
        Spacer(1, 7),
        Paragraph(opening, s["lead"]),
    ]

    left_column = []
    add_heading(left_column, "What is established", s["section"])
    left_column.append(Paragraph(fixed, s["body"]))
    add_heading(left_column, "Make the character your own", s["section"])
    left_column.append(panel(custom, doc.width / 2 - 10, s["body"]))
    add_heading(left_column, "Decide before play", s["section"])
    for question in questions:
        left_column.append(Paragraph(f"- {question}", s["prompt"]))

    section_blocks = []
    for heading, paragraphs in sections.items():
        if heading in {"Bio", "Stats", *REQUIRED_SECTIONS}:
            continue
        block = [Paragraph(heading.upper(), s["section"])]
        for index, paragraph in enumerate(paragraphs):
            paragraph = inline_markdown(paragraph)
            if index == 0 and (heading.startswith("Weakness") or heading.startswith("Gift") or heading.startswith("Tool")):
                paragraph_style = s["quote"]
            elif heading == "Secret":
                paragraph_style = s["secret"]
            else:
                paragraph_style = s["small"]
            block.append(Paragraph(paragraph, paragraph_style))
        if heading == "Secret":
            # Leave an actual place to begin writing instead of presenting only
            # an instruction. The Dreamer's denser rules support one line; the
            # other packets have room for two.
            line_count = 1 if compact else 2
            for _ in range(line_count):
                block.append(Paragraph("_" * 48, s["secret_line"]))
        section_blocks.append(block)

    # Choose one reading-order split between complete sections. Identity and
    # customization remain first in the left column; the character mechanics
    # may continue beneath them when that produces a more even page. Secret
    # always remains in the right column. No section is divided between columns.
    column_content_width = doc.width / 2 - 13
    candidates = []
    for split_at in range(len(section_blocks)):
        candidate_left = left_column + [item for block in section_blocks[:split_at] for item in block]
        candidate_right = [item for block in section_blocks[split_at:] for item in block]
        left_height = stack_height(candidate_left, column_content_width)
        right_height = stack_height(candidate_right, column_content_width)
        candidates.append((abs(left_height - right_height), max(left_height, right_height), split_at))

    _, _, split_at = min(candidates)
    left_column.extend(item for block in section_blocks[:split_at] for item in block)
    right_column = [item for block in section_blocks[split_at:] for item in block]

    columns = Table(
        [[left_column, right_column]],
        colWidths=[doc.width / 2 - 5, doc.width / 2 - 5],
        hAlign="LEFT",
    )
    columns.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, -1), 0),
        ("RIGHTPADDING", (0, 0), (0, -1), 8),
        ("LEFTPADDING", (1, 0), (1, -1), 8),
        ("RIGHTPADDING", (1, 0), (1, -1), 0),
        ("LINEBEFORE", (1, 0), (1, -1), 0.45, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(columns)

    quick_reference = []
    add_heading(quick_reference, "Quick play reference", s["section"])
    reference_left = [
        Paragraph(
            "<b>Tests.</b> Use your active Premonition, add the named Stat, and compare the total with the Difficulty. "
            "Beat it by 3 for a clean success; meet it or beat it by 1-2 for success with a consequence; below it fails.",
            s["reference"],
        ),
        Paragraph(
            "<b>Minor cards.</b> Ace: critical success and regain 1 Grounding. Page 11. Knight 12. Queen: automatic success and lose 1 Grounding. King: critical failure and lose 1 Grounding.",
            s["reference"],
        ),
    ]
    reference_right = [
        Paragraph(
            "<b>Major Arcana.</b> A Major is never a test value. It changes the whole house, then every character resets their Premonition.",
            s["reference"],
        ),
        Paragraph(
            "<b>Grounding.</b> Begin with 6. At 0, you are Unmoored and draw blindly until an Ace or meaningful help in a place of safety restores you.",
            s["reference"],
        ),
        Paragraph(
            "<b>Tools.</b> Use your Tool in any physically reasonable way. No test is needed when it makes the outcome safe and certain.",
            s["reference"],
        ),
    ]
    ref = Table([[reference_left, reference_right]], colWidths=[doc.width / 2, doc.width / 2], hAlign="LEFT")
    ref.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.65, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
    ]))
    quick_reference.append(ref)

    stat_definitions = [
        ("NERVE", "Endurance, courage, and sanity"),
        ("NOTICE", "Perception and awareness"),
        ("RAPPORT", "Charisma and social influence"),
        ("REASON", "Intelligence, knowledge, and willpower"),
        ("VIGOR", "Strength, dexterity, and athletics"),
    ]
    stat_cells = [
        [Paragraph(name, s["stat_ref_name"]), Paragraph(description, s["stat_ref_body"])]
        for name, description in stat_definitions
    ]
    stat_ref = Table([stat_cells], colWidths=[doc.width / 5] * 5, hAlign="LEFT")
    stat_ref.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("BOX", (0, 0), (-1, -1), 0.65, RULE),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, RULE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    quick_reference.append(stat_ref)

    # A one-cell table keeps the heading, rules box, and stat strip indivisible.
    # TopPadder then expands only the space above that single grouped object.
    bottom_group = Table([[quick_reference]], colWidths=[doc.width], hAlign="LEFT")
    bottom_group.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    story.append(TopPadder(bottom_group))

    doc.build(story)
    return output


def build():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return [build_packet(slug, filename) for slug, filename in SELECTED.items()]


if __name__ == "__main__":
    for path in build():
        print(path)
