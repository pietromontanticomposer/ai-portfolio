from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Flowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
OUTPUT_EN = OUTPUT_DIR / "Pietro-Montanti-AI-Resume.pdf"
OUTPUT_IT = OUTPUT_DIR / "Pietro-Montanti-CV-AI-Italiano.pdf"
OUTPUT_BILINGUAL = OUTPUT_DIR / "Pietro-Montanti-AI-Resume-Bilingual.pdf"
PHOTO = ROOT / "assets" / "pietro-montanti-venice.png"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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
title = ParagraphStyle("Title", parent=styles["Title"], fontName=BODY_FONT, fontSize=24, leading=26, textColor=INK, alignment=TA_LEFT, spaceAfter=3)
subtitle = ParagraphStyle("Subtitle", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=9.2, leading=11.5, textColor=GREEN)
contact = ParagraphStyle("Contact", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=7.2, leading=10.5, textColor=MUTED, alignment=TA_RIGHT)
section = ParagraphStyle("Section", parent=styles["Heading2"], fontName=BODY_FONT, fontSize=8.2, leading=10, textColor=GREEN, spaceBefore=8, spaceAfter=4, uppercase=True, tracking=1.0)
body = ParagraphStyle("Body", parent=styles["BodyText"], fontName=BODY_FONT, fontSize=8.4, leading=11.3, textColor=INK, spaceAfter=3)
project_name = ParagraphStyle("Project", parent=body, fontName=BODY_FONT, fontSize=8.7, leading=11, textColor=INK)
small = ParagraphStyle("Small", parent=body, fontSize=7.2, leading=9.5, textColor=MUTED)


class Portrait(Flowable):
    """Rounded document crop; the source photo remains unaltered."""

    def __init__(self, path, width=28 * mm, height=36 * mm):
        super().__init__()
        self.path = path
        self.width = width
        self.height = height

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        clip = canvas.beginPath()
        clip.roundRect(0, 0, self.width, self.height, 2.5 * mm)
        canvas.clipPath(clip, stroke=0, fill=0)

        crop_width = 300
        crop_height = 390
        crop_x = 75
        crop_from_top = 45
        image_width = self.width * 450 / crop_width
        image_height = self.height * 600 / crop_height
        image_x = -self.width * crop_x / crop_width
        image_y = -self.height * (600 - crop_from_top - crop_height) / crop_height
        canvas.drawImage(ImageReader(str(self.path)), image_x, image_y, image_width, image_height, mask="auto")
        canvas.restoreState()
        canvas.setStrokeColor(GREEN)
        canvas.setLineWidth(1)
        canvas.roundRect(0, 0, self.width, self.height, 2.5 * mm, stroke=1, fill=0)


COPY = {
    "en": {
        "subtitle": "Applied AI Workflow Designer · LLM Evaluator · Italian Language Specialist",
        "location": "Italy · Remote",
        "github_profile_label": "github.com/pietromontanticomposer",
        "github_source_label": "github.com/pietromontanticomposer/ai-portfolio",
        "profile_label": "PROFILE",
        "profile": "Italian native speaker with a diploma in clarinet (110/110) and 13 years of professional experience across composition, performance and events. I began using AI to solve concrete production, review and organizational problems; that work evolved into designing and testing AI-assisted products with measurable quality checks, deterministic guardrails and human approval.",
        "projects_label": "SELECTED AI-ASSISTED PROJECTS",
        "projects": [
            ("AI Outreach CRM", "Designed a multi-model workflow combining web retrieval, personalized drafting, independent Claude/Codex review, citation checks and human approval. Built with Next.js, TypeScript, Supabase and Vercel."),
            ("Interpelli Watcher", "Created a fail-closed document automation workflow using official sources, XML/PDF extraction, OCR, eligibility rules and dual-model approval. Validated with 83 deterministic tests."),
            ("MailPilot", "Built an Electron email client with persistent IMAP sync, CRM enrichment, AI-generated editable drafts, provider fallback and explicit approval before sending."),
            ("Suno MIDI Extractor", "Developed an audio-to-MIDI desktop pipeline using PyTorch-based transcription, FFmpeg, deduplication and experimental sustain-pedal reconstruction."),
        ],
        "capabilities_label": "CAPABILITIES",
        "quality_title": "AI & quality",
        "quality": "LLM evaluation · Prompt design · Structured outputs · Retrieval grounding · Hallucination checks · Safety review · Human-in-the-loop workflows · Test design",
        "technical_title": "Technical exposure",
        "technical": "ChatGPT · Claude · Codex · Gemini · Next.js · TypeScript · Python · Electron · Supabase · Vercel · Git/GitHub · IMAP/SMTP",
        "background_label": "LANGUAGES & PROFESSIONAL BACKGROUND",
        "languages_title": "Languages",
        "languages": "Italian: native<br/>English: advanced comprehension, intermediate spoken communication",
        "background_title": "Professional background",
        "background": "Independent composer, clarinetist and saxophonist. Creative production experience sharpened my ability to translate ambiguous requirements into structured, testable workflows and clear deliverables.",
        "disclosure": "Development approach: AI-assisted implementation with direct ownership of requirements, workflow design, testing, debugging and final quality decisions.",
        "document_title": "Pietro Montanti - AI Resume",
    },
    "it": {
        "subtitle": "Progettista di workflow AI applicati · Valutatore LLM · Specialista di lingua italiana",
        "location": "Italia · Da remoto",
        "github_profile_label": "github.com/pietromontanticomposer",
        "github_source_label": "github.com/pietromontanticomposer/ai-portfolio",
        "profile_label": "PROFILO",
        "profile": "Madrelingua italiano, diplomato in clarinetto con 110/110, con 13 anni di esperienza professionale tra composizione, performance ed eventi. Ho iniziato a usare l'AI per risolvere problemi concreti di produzione, revisione e organizzazione; quel percorso si è evoluto nella progettazione e nel collaudo di prodotti assistiti dall'AI con controlli di qualità misurabili, regole deterministiche e approvazione umana.",
        "projects_label": "PROGETTI SELEZIONATI ASSISTITI DALL'AI",
        "projects": [
            ("AI Outreach CRM", "Progettato un workflow multimodale che combina ricerca web, stesura personalizzata, revisione indipendente Claude/Codex, controllo delle citazioni e approvazione umana. Sviluppato con Next.js, TypeScript, Supabase e Vercel."),
            ("Interpelli Watcher", "Creato un workflow documentale fail-closed basato su fonti ufficiali, estrazione XML/PDF, OCR, regole di idoneità e approvazione di due modelli. Validato con 83 test deterministici."),
            ("MailPilot", "Realizzato un client email Electron con sincronizzazione IMAP persistente, arricchimento CRM, bozze AI modificabili, provider di riserva e approvazione esplicita prima dell'invio."),
            ("Suno MIDI Extractor", "Sviluppata una pipeline desktop da audio a MIDI con trascrizione basata su PyTorch, FFmpeg, deduplicazione e ricostruzione sperimentale del pedale di sustain."),
        ],
        "capabilities_label": "COMPETENZE",
        "quality_title": "AI e qualità",
        "quality": "Valutazione LLM · Progettazione prompt · Output strutturati · Grounding su fonti · Controllo allucinazioni · Revisione sicurezza · Workflow con supervisione umana · Progettazione test",
        "technical_title": "Tecnologie",
        "technical": "ChatGPT · Claude · Codex · Gemini · Next.js · TypeScript · Python · Electron · Supabase · Vercel · Git/GitHub · IMAP/SMTP",
        "background_label": "LINGUE E PROFILO PROFESSIONALE",
        "languages_title": "Lingue",
        "languages": "Italiano: madrelingua<br/>Inglese: comprensione avanzata, conversazione di livello intermedio",
        "background_title": "Profilo professionale",
        "background": "Compositore, clarinettista e sassofonista indipendente. L'esperienza nella produzione creativa ha rafforzato la capacità di trasformare richieste ambigue in workflow strutturati, verificabili e orientati a risultati chiari.",
        "disclosure": "Approccio allo sviluppo: implementazione assistita dall'AI, con responsabilità diretta su requisiti, progettazione del workflow, test, debugging e decisioni finali sulla qualità.",
        "document_title": "Pietro Montanti - Curriculum AI",
    },
}


def build_resume(output_path, language):
    copy = COPY[language]
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=13 * mm,
        bottomMargin=12 * mm,
        title=copy["document_title"],
        author="Pietro Montanti",
    )

    identity = Table(
        [[Paragraph("Pietro Montanti", title)], [Paragraph(copy["subtitle"], subtitle)]],
        colWidths=[78 * mm],
    )
    identity.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    header = Table(
        [[Portrait(PHOTO), identity, Paragraph(
            '<link href="mailto:pietromontanticomposer@gmail.com" color="#596159">pietromontanticomposer@gmail.com</link><br/>'
            '<link href="https://pietro-ai-portfolio.vercel.app" color="#1D4F3A">pietro-ai-portfolio.vercel.app</link><br/>'
            f'<link href="https://github.com/pietromontanticomposer" color="#1D4F3A">{copy["github_profile_label"]}</link><br/>'
            f'<link href="https://github.com/pietromontanticomposer/ai-portfolio" color="#1D4F3A">{copy["github_source_label"]}</link><br/>'
            + copy["location"],
            contact,
        )]],
        colWidths=[32 * mm, 78 * mm, 55 * mm],
    )
    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, GREEN),
    ]))

    story = [header]
    story.append(Paragraph(copy["profile_label"], section))
    story.append(Paragraph(copy["profile"], body))
    story.append(Paragraph(copy["projects_label"], section))

    for name, description in copy["projects"]:
        row = Table([[Paragraph(f"<b>{name}</b>", project_name), Paragraph(description, body)]], colWidths=[38 * mm, 127 * mm])
        row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
        story.append(KeepTogether(row))

    story.append(Paragraph(copy["capabilities_label"], section))
    capabilities = Table([
        [Paragraph(f'<b>{copy["quality_title"]}</b><br/>{copy["quality"]}', body),
         Paragraph(f'<b>{copy["technical_title"]}</b><br/>{copy["technical"]}', body)]
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

    story.append(Paragraph(copy["background_label"], section))
    background = Table([
        [Paragraph(f'<b>{copy["languages_title"]}</b><br/>{copy["languages"]}', body),
         Paragraph(f'<b>{copy["background_title"]}</b><br/>{copy["background"]}', body)]
    ], colWidths=[62 * mm, 103 * mm])
    background.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 10)]))
    story.append(background)

    story.append(Spacer(1, 5 * mm))
    story.append(Paragraph(copy["disclosure"], small))
    doc.build(story)


def build_bilingual_pdf():
    writer = PdfWriter()
    for source in (OUTPUT_EN, OUTPUT_IT):
        reader = PdfReader(str(source))
        writer.add_page(reader.pages[0])
    writer.add_metadata({
        "/Title": "Pietro Montanti - Bilingual AI Resume",
        "/Author": "Pietro Montanti",
        "/Subject": "English and Italian AI resume",
    })
    with OUTPUT_BILINGUAL.open("wb") as target:
        writer.write(target)


build_resume(OUTPUT_EN, "en")
build_resume(OUTPUT_IT, "it")
build_bilingual_pdf()
print(OUTPUT_EN)
print(OUTPUT_IT)
print(OUTPUT_BILINGUAL)
