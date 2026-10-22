import pytest
from reportlab.pdfgen import canvas

from sift.cli import main


def test_parse_command_prints_blocks(tmp_path, capsys):
    path = tmp_path / "os_lec03.pdf"
    c = canvas.Canvas(str(path))
    c.drawString(100, 750, "Deadlock")
    c.showPage()
    c.save()

    main(["parse", str(path)])

    output = capsys.readouterr().out

    assert "os_lec03-s1-b1" in output
    assert "Deadlock" in output

def test_parse_command_exits_on_missing_file():
    with pytest.raises(SystemExit):
        main(["parse", "does_not_exist.pdf"])

def test_parse_command_exits_on_unsupported_type(tmp_path):
    path = tmp_path / "notes.xyz"
    path.write_text("x")

    with pytest.raises(SystemExit):
        main(["parse", str(path)])