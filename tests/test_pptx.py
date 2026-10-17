from pptx import Presentation

from sift.parsing.pptx_parser import parse_pptx


def test_parse_pptx_reads_title_and_bullets(tmp_path):
    path = tmp_path / "os_lec03.pptx"

    prs = Presentation()
    slide_layout = prs.slide_layouts[1]  # Title and Content layout
    slide = prs.slides.add_slide(slide_layout)

    slide.shapes.title.text = "Deadlock"

    body = slide.placeholders[1].text_frame
    body.text = "Mutual exclusion"
    body.add_paragraph().text = "Hold and wait"

    prs.save(path)

    blocks = parse_pptx(path)

    assert [b.text for b in blocks] == ["Deadlock", "Mutual exclusion", "Hold and wait"]
    assert blocks[0].block_type == "title"
    assert blocks[1].id == "os_lec03-s1-b2"