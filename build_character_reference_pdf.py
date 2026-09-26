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
    FrameBreak,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output" / "pdf" / "mourning-bluff-manor-character-reference.pdf"

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
    title = clean(re.search(r"^# (.+)$", text, re.MULTILINE).group(1))
    parts = re.split(r"^## (.+)$", text, flags=re.MULTILINE)
    sections = {}
    for index in range(1, len(parts), 2):
        heading = clean(parts[index])
        heading = re.sub(r"^(Weakness|Gift|Tool)\s*[,:-]\s*", r"\1: ", heading)
        sections[heading] = [
            p.strip() for p in clean(parts[index + 1].strip()).split("\n\n") if p.strip()
        ]
    tool_heading = next(heading for heading in sections if heading.startswith("Tool: "))
    tool_description = sections[tool_heading][0]
    return title, sections["Bio"], sections["Stats"][0].replace("**", ""), tool_description


def draw_page(canvas, doc):
    canvas.saveState()
    width, height = letter
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, width, height, stroke=0, fill=1)

    center_x = width / 2
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.8)
    canvas.line(center_x, 0.62 * inch, center_x, height - 0.48 * inch)

    canvas.setStrokeColor(RUST)
    canvas.setLineWidth(1.1)
    canvas.line(0.55 * inch, 0.43 * inch, width - 0.55 * inch, 0.43 * inch)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(0.58 * inch, 0.25 * inch, "MOURNING BLUFF MANOR")
    canvas.drawRightString(width - 0.58 * inch, 0.25 * inch, f"CHARACTER REFERENCE  |  {doc.page}")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    page_width, _ = letter
    outer = 0.55 * inch
    gutter = 0.34 * inch
    frame_width = (page_width - 2 * outer - gutter) / 2

    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=outer,
        rightMargin=outer,
        topMargin=0.48 * inch,
        bottomMargin=0.58 * inch,
        title="Mourning Bluff Manor Character Reference",
        author="Michael Wells",
        subject="Two-column character biographies, tools, and stats",
    )

    frames = [
        Frame(
            outer,
            doc.bottomMargin,
            frame_width,
            doc.height,
            leftPadding=0,
            rightPadding=gutter / 2,
            topPadding=0,
            bottomPadding=0,
            id="left",
        ),
        Frame(
            outer + frame_width + gutter,
            doc.bottomMargin,
            frame_width,
            doc.height,
            leftPadding=gutter / 2,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            id="right",
        ),
    ]
    doc.addPageTemplates([PageTemplate(id="reference", frames=frames, onPage=draw_page)])

    name_style = ParagraphStyle(
        "Name",
        fontName="Times-Bold",
        fontSize=15,
        leading=17,
        textColor=INK,
        alignment=TA_CENTER,
        spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "Body",
        fontName="Times-Roman",
        fontSize=8.15,
        leading=10.05,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=3,
    )
    tool_flavor_style = ParagraphStyle(
        "ToolFlavor",
        parent=body_style,
        fontName="Times-Italic",
        textColor=colors.HexColor("#4D4037"),
    )
    stats_style = ParagraphStyle(
        "Stats",
        fontName="Helvetica-Bold",
        fontSize=7.7,
        leading=9,
        textColor=INK,
        alignment=TA_CENTER,
    )

    story = []
    for index, filename in enumerate(CHARACTERS):
        if index == 5:
            story.append(PageBreak())
        elif index in (3, 8):
            story.append(FrameBreak())
        title, bio, stats, tool_description = parse_profile(ROOT / "cast" / filename)
        block = [Paragraph(title, name_style)]

        stats_table = Table([[Paragraph(stats, stats_style)]], colWidths=[frame_width - gutter / 2])
        stats_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), PANEL),
                    ("BOX", (0, 0), (-1, -1), 0.6, RULE),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        block.extend([stats_table, Spacer(1, 5)])
        for paragraph in bio:
            block.append(Paragraph(paragraph, body_style))
        block.append(Paragraph(inline_markdown(tool_description), tool_flavor_style))

        if index < len(CHARACTERS) - 1:
            block.extend(
                [
                    Spacer(1, 7),
                    HRFlowable(width="100%", thickness=0.65, color=RULE, spaceBefore=0, spaceAfter=9),
                ]
            )
        story.append(KeepTogether(block))

    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    print(build())
