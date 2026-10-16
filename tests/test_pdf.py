import pytest


@pytest.mark.skip(reason="parser not implemented")
def test_parse_pdf_creates_blocks_and_skips_empty_pages(tmp_path):
    # Create a sample PDF file with two pages, one empty and one with text
    return
