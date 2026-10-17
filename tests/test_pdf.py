from reportlab.pdfgen import canvas

from sift.parsing.pdf import parse_pdf


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