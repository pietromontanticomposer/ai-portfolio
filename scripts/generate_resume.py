from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Pietro-Montanti-AI-Resume.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

INK = colors.HexColor("#111712")
GREEN = colors.HexColor("#1D4F3A")
MUTED = colors.HexColor("#596159")
LINE = colors.HexColor("#CCD2C8")
PALE = colors.HexColor("#EEF2EA")

font_dir = Path("/System/Library/Fonts")
regular = font_dir / "Helvetica.ttc"
if regular.exists():
    try:
        pdfmetrics.registerFont(TTFont("ResumeSans", str(regular), subfontIndex=0))
        BODY_FONT = "ResumeSans"
    except Exception:
        BODY_FONT = "Helvetica"
else:
    BODY_FONT = "Helvetica"

styles = getSampleStyleSheet()
title = ParagraphStyle("Title", parent=styles["Title"], fontName=BODY_FONT, fontSize=25, leading=27, textColor=INK, alignment=TA_LEFT, spaceAfter=2)
subtitle = ParagraphStyle("Subtitle", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=9.5, leading=12, textColor=GREEN)
contact = ParagraphStyle("Contact", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=7.5, leading=11, textColor=MUTED, alignment=TA_RIGHT)
section = ParagraphStyle("Section", parent=styles["Heading2"], fontName=BODY_FONT, fontSize=8.2, leading=10, textColor=GREEN, spaceBefore=8, spaceAfter=4, uppercase=True, tracking=1.0)
body = ParagraphStyle("Body", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=8.4, leading=11.3, textColor=INK, spaceAfter=3)
project_name = ParagraphStyle("Project", parent=body, fontName=BODY_FONT, fontSize=8.7, leading=11, textColor=INK)
small = ParagraphStyle("Small", parent=body, fontSize=7.2, leading=9.5, textColor=MUTED)

doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=16 * mm,
    rightMargin=16 * mm,
    topMargin=13 * mm,
    bottomMargin=12 * mm,
    title="Pietro Montanti - AI Resume",
    author="Pietro Montanti",
)

story = []
header = Table(
    [[Paragraph("Pietro Montanti", title), Paragraph("pietromontanticomposer@gmail.com<br/>Italy · Remote", contact)],
     [Paragraph("AI Workflow Builder · LLM Evaluator · Italian Language Specialist", subtitle), ""]],
    colWidths=[112 * mm, 53 * mm],
)
header.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("SPAN", (1, 0), (1, 1)),
    ("LINEBELOW", (0, 1), (-1, 1), 1.5, GREEN),
    ("BOTTOMPADDING", (0, 1), (-1, 1), 7),
]))
story.append(header)

story.append(Paragraph("PROFILE", section))
story.append(Paragraph(
    "Italian native speaker with hands-on experience designing, testing and refining AI-assisted products. Strong focus on instruction following, output quality, retrieval-grounded generation, deterministic guardrails and human approval before real-world actions.",
    body,
))

story.append(Paragraph("SELECTED AI-ASSISTED PROJECTS", section))
projects = [
    ("AI Outreach CRM", "Designed a multi-model workflow combining web retrieval, personalized drafting, independent Claude/Codex review, citation checks and human approval. Built with Next.js, TypeScript, Supabase and Vercel."),
    ("Interpelli Watcher", "Created a fail-closed document automation workflow using official sources, XML/PDF extraction, OCR, eligibility rules and dual-model approval. Validated with 83 deterministic tests."),
    ("MailPilot", "Built an Electron email client with persistent IMAP sync, CRM enrichment, AI-generated editable drafts, provider fallback and explicit approval before sending."),
    ("Suno MIDI Extractor", "Developed an audio-to-MIDI desktop pipeline using PyTorch-based transcription, FFmpeg, deduplication and experimental sustain-pedal reconstruction."),
]
for name, description in projects:
    row = Table([[Paragraph(f"<b>{name}</b>", project_name), Paragraph(description, body)]], colWidths=[38 * mm, 127 * mm])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    story.append(KeepTogether(row))

story.append(Paragraph("CAPABILITIES", section))
capabilities = Table([
    [Paragraph("<b>AI & quality</b><br/>LLM evaluation · Prompt design · Structured outputs · Retrieval grounding · Hallucination checks · Safety review · Human-in-the-loop workflows · Test design", body),
     Paragraph("<b>Technical exposure</b><br/>ChatGPT · Claude · Codex · Gemini · Next.js · TypeScript · Python · Electron · Supabase · Vercel · Git/GitHub · IMAP/SMTP", body)]
], colWidths=[82.5 * mm, 82.5 * mm])
capabilities.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BACKGROUND", (0, 0), (-1, -1), PALE),
    ("BOX", (0, 0), (-1, -1), 0.5, LINE),
    ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
    ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
]))
story.append(capabilities)

story.append(Paragraph("LANGUAGES & PROFESSIONAL BACKGROUND", section))
background = Table([
    [Paragraph("<b>Languages</b><br/>Italian: native<br/>English: advanced comprehension, intermediate spoken communication", body),
     Paragraph("<b>Professional background</b><br/>Independent composer and multi-instrumentalist. Experienced in translating complex creative requirements into structured, testable production workflows.", body)]
], colWidths=[62 * mm, 103 * mm])
background.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
story.append(background)

story.append(Spacer(1, 5 * mm))
story.append(Paragraph(
    "Development approach: AI-assisted implementation with direct ownership of requirements, workflow design, testing, debugging and final quality decisions.",
    small,
))

doc.build(story)
print(OUTPUT)
