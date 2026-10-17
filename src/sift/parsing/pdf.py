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

    deck = path.stem.lower()
    blocks = []

    for page_number, page in enumerate(PdfReader(path).pages, start=1):
        text = page.extract_text() or ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for index, line in enumerate(lines, start=1):
            block = SlideBlock(
                id=f"{deck}-s{page_number}-b{index}",
                slide_number=page_number,
                text=line,
            )
            blocks.append(block)

    return blocks
