from pathlib import Path

from pypdf import PdfReader

from sift.models import SlideBlock


def parse_pdf(path: Path) -> list[SlideBlock]:
    """Parse a PDF file and extract slide blocks.

    Args:
        path (Path): The path to the PDF file.

    Returns:
        list[SlideBlock]: A list of slide blocks extracted from the PDF file.
    """

    reader = PdfReader(path)
    blocks = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text() or ""

        if not text.strip():
            continue

        blocks.append(
            SlideBlock(
                id=f"{path.stem}-page-{page_number + 1}",
                slide_number=page_number + 1,
                text=text.strip(),
            )
        )

    return blocks
