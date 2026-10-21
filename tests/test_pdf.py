from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas

from sift.parsing.pdf_parser import parse_pdf


def test_parse_pdf_creates_blocks_and_skips_empty_pages(tmp_path):
    path = tmp_path / "os_lec03.pdf"

    c = canvas.Canvas(str(path))
    c.drawString(100, 750, "Deadlock")
    c.drawString(100, 720, "Four necessary conditions for deadlock")
    c.showPage()  # Create a new page (empty)
    c.showPage()  # Create another new page (empty)
    c.drawString(100, 750, "Banker's algorithm")
    c.showPage()  # Create a new page (empty)
    c.save()

    blocks = parse_pdf(path)

    assert {b.slide_number for b in blocks} == {1, 3}
    assert blocks[0].id == "os_lec03-s1-b1"
    assert blocks[0].text == "Deadlock"

def test_parse_pdf_extracts_images_as_blocks(tmp_path):
    img_path = tmp_path / "diagram.png"
    Image.new("RGB", (10, 10)).save(img_path)

    path = tmp_path / "os_lec03.pdf"
    c = canvas.Canvas(str(path))
    c.drawImage(str(img_path), 100, 500, width=100, height=100)
    c.showPage()
    c.save()

    out_dir = tmp_path / "images"
    blocks = parse_pdf(path, image_dir=out_dir)

    assert len(blocks) == 1
    assert blocks[0].id == "os_lec03-s1-b1"
    assert blocks[0].block_type == "image"
    assert blocks[0].text == ""
    assert Path(blocks[0].metadata["image_path"]).exists()