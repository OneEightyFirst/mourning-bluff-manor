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
OUTPUT = ROOT / "output" / "pdf" / "mourning-bluff-manor-character-profiles.pdf"

CHARACTERS = [
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
        "&": "&amp;",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def inline_markdown(text):
    if text.startswith("*") and text.endswith("*") and not text.startswith("**"):
        return f"<i>{text[1:-1]}</i>"
    return text


def parse_profile(path):
    text = path.read_text(encoding="utf-8")
    title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
    title = clean(title_match.group(1))
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    sections = {}
    for index in range(1, len(parts), 2):
        heading = clean(parts[index])
        heading = re.sub(r"^(Weakness|Gift|Tool)\s*[,:-]\s*", r"\1: ", heading)
        body = clean(parts[index + 1].strip())
        sections[heading] = [p.strip() for p in body.split("\n\n") if p.strip()]
    return title, sections


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, letter[0], letter[1], stroke=0, fill=1)
    canvas.setStrokeColor(RUST)
    canvas.setLineWidth(1.2)
    canvas.line(0.62 * inch, 0.48 * inch, 7.88 * inch, 0.48 * inch)
    canvas.setFont("Helvetica", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.65 * inch, 0.28 * inch, "MOURNING BLUFF MANOR")
    canvas.drawRightString(7.85 * inch, 0.28 * inch, f"CHARACTER {doc.page} OF 10")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.68 * inch,
        rightMargin=0.68 * inch,
        topMargin=0.48 * inch,
        bottomMargin=0.62 * inch,
        title="Mourning Bluff Manor Character Profiles",
        author="Michael Wells",
        subject="Ten complete character profiles",
    )
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )
    doc.addPageTemplates([PageTemplate(id="character", frames=[frame], onPage=draw_page)])

    title_style = ParagraphStyle(
        "Title",
        fontName="Times-Bold",
        fontSize=22,
        leading=24,
        textColor=INK,
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    kicker_style = ParagraphStyle(
        "Kicker",
        fontName="Helvetica-Bold",
        fontSize=6.8,
        leading=8,
        tracking=1.7,
        textColor=RUST,
        alignment=TA_CENTER,
        spaceAfter=9,
    )
    section_style = ParagraphStyle(
        "Section",
        fontName="Helvetica-Bold",
        fontSize=8.3,
        leading=10,
        textColor=RUST,
        spaceBefore=5,
        spaceAfter=2.5,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName="Times-Roman",
        fontSize=8.65,
        leading=10.85,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=3.2,
    )
    motivation_style = ParagraphStyle(
        "Motivation",
        parent=body_style,
        fontName="Times-Italic",
        textColor=colors.HexColor("#4D4037"),
        borderColor=RULE,
        borderWidth=0,
        borderPadding=(0, 0, 0, 7),
    )
    stats_style = ParagraphStyle(
        "Stats",
        fontName="Helvetica-Bold",
        fontSize=9.2,
        leading=11,
        textColor=INK,
        alignment=TA_CENTER,
    )
    secret_style = ParagraphStyle(
        "Secret",
        parent=body_style,
        fontSize=8.2,
        leading=10,
        textColor=MUTED,
    )

    story = []
    for character_index, filename in enumerate(CHARACTERS):
        title, sections = parse_profile(ROOT / "cast" / filename)
        story.append(Paragraph(title, title_style))
        story.append(Paragraph("CHARACTER DOSSIER", kicker_style))

        bio = sections.pop("Bio")
        story.append(Paragraph("BIO", section_style))
        for paragraph in bio:
            story.append(Paragraph(paragraph, body_style))

        stats = sections.pop("Stats")[0].replace("**", "")
        stats_table = Table([[Paragraph(stats, stats_style)]], colWidths=[doc.width])
        stats_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                    ("BOX", (0, 0), (-1, -1), 0.7, RULE),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.extend([Spacer(1, 4), stats_table, Spacer(1, 4)])

        for heading, paragraphs in sections.items():
            is_secret = heading == "Secret"
            block = [Paragraph(heading.upper(), section_style)]
            for paragraph_index, paragraph in enumerate(paragraphs):
                paragraph = inline_markdown(paragraph)
                if is_secret:
                    style = secret_style
                elif heading.startswith("Weakness") and paragraph_index == 0:
                    style = motivation_style
                elif heading.startswith("Gift") and paragraph_index == 0:
                    style = motivation_style
                else:
                    style = body_style
                block.append(Paragraph(paragraph, style))
            story.append(KeepTogether(block))

        if character_index < len(CHARACTERS) - 1:
            story.append(PageBreak())

    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(build())
