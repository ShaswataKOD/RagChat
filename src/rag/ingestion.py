from pathlib import Path
import re

import pymupdf


def clean_text(text: str) -> str:
    """Normalize whitespace while preserving line breaks."""

    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Normalize spaces and tabs without removing newlines.
    text = re.sub(r"[^\S\n]+", " ", text)

    # Remove unnecessary whitespace around lines.
    text = "\n".join(line.strip() for line in text.split("\n"))

    # Collapse excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""

    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("The supplied file must be a PDF.")

    pages = []

    with pymupdf.open(pdf_path) as document:
        if document.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            # Correct escape characters only if genuinely present.
            text = text.replace("\\'", "'").replace('\\"', '"')

            text = clean_text(text)

            if text:
                pages.append(
                    {
                        "page_number": page_number,
                        "text": text,
                    }
                )

    if not pages:
        raise ValueError(
            "No extractable text found in the PDF. It may be scanned or empty."
        )

    return pages


# pages = extract_text_from_pdf("C:/Users/shasw/Downloads/CV.pdf")

# print(pages)
