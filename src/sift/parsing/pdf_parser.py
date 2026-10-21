from pathlib import Path

from pypdf import PdfReader

from sift.models import SlideBlock


def parse_pdf(path: Path, image_dir: Path | None = None) -> list[SlideBlock]:
    """Parse a PDF file and extract slide blocks.

    Args:
        path (Path): The path to the PDF file.
        image_dir (Path | None): Folder to save extracted images into. If None, images are still returned as blocks but are not written to disk.

    Returns:
        list[SlideBlock]: One block per non-empty text line, plus one block per embedded image.
    """

    deck = path.stem.lower()
    blocks = []

    for page_number, page in enumerate(PdfReader(path).pages, start=1):
        counter = 0 # Restarts on every page

        text = page.extract_text() or ""
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        for line in lines:
            counter += 1
            blocks.append(
                SlideBlock(
                    id=f"{deck}-s{page_number}-b{counter}",
                    slide_number=page_number,
                    text=line
                )
            )

        for image in page.images:
            counter += 1
            block_id = f"{deck}-s{page_number}-b{counter}"
            block = SlideBlock (
                id=block_id,
                slide_number=page_number,
                text="",
                block_type="image"
            )

            if image_dir is not None:
                image_dir.mkdir(parents=True, exist_ok=True)
                image_path = image_dir / f"{block_id}{Path(image.name).suffix}"
                image_path.write_bytes(image.data)
                block.metadata["image_path"] = str(image_path)

            blocks.append(block)

    return blocks
