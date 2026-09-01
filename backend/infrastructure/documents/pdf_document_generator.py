from html import escape
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from backend.domain.enums.document_format import (
    DocumentFormat,
)
from backend.domain.interfaces.document_generator import (
    IDocumentGenerator,
)


class PdfDocumentGenerator(IDocumentGenerator):
    @property
    def document_format(self) -> DocumentFormat:
        """
        Return the PDF document format.
        """
        return DocumentFormat.PDF

    @property
    def media_type(self) -> str:
        """
        Return the PDF MIME type.
        """
        return "application/pdf"

    @property
    def file_extension(self) -> str:
        """
        Return the PDF file extension.
        """
        return "pdf"

    def generate(
        self,
        title: str,
        content: str,
    ) -> bytes:
        """
        Generate a PDF document in memory.
        """
        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
            title=title,
            author="Raissa AI",
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "RaissaTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=25,
            spaceAfter=20,
        )

        body_style = ParagraphStyle(
            "RaissaBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=17,
            spaceAfter=8,
        )

        heading_style = ParagraphStyle(
            "RaissaHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            spaceBefore=8,
            spaceAfter=8,
        )

        story = [
            Paragraph(
                escape(title),
                title_style,
            ),
            Paragraph(
                "Resumo organizado pela Raissa AI",
                body_style,
            ),
            Spacer(1, 10),
        ]

        for raw_line in content.splitlines():
            line = raw_line.strip()

            if not line:
                story.append(
                    Spacer(1, 6)
                )
                continue

            if line.startswith("#"):
                heading = line.lstrip(
                    "#"
                ).strip()

                story.append(
                    Paragraph(
                        escape(heading),
                        heading_style,
                    )
                )
                continue

            if line.startswith(("- ", "* ")):
                text = line[2:].strip()

                story.append(
                    Paragraph(
                        f"• {escape(text)}",
                        body_style,
                    )
                )
                continue

            story.append(
                Paragraph(
                    escape(line),
                    body_style,
                )
            )

        document.build(story)

        buffer.seek(0)

        return buffer.getvalue()