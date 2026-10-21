from pathlib import Path

from sift.models import SlideBlock
from sift.parsing.pdf_parser import parse_pdf
from sift.parsing.pptx_parser import parse_pptx

PARSERS = {".pdf": parse_pdf, ".pptx": parse_pptx}


def parse_document(path: Path, image_dir: Path | None = None) -> list[SlideBlock]:
    suffix = path.suffix.lower()

    if suffix not in PARSERS:
        raise ValueError(f"Unsupported file type: {suffix}")

    return PARSERS[suffix](path, image_dir=image_dir)