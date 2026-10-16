from sift.models import SlideBlock


def test_slide_block_defaults():
    block = SlideBlock(
        id="block-1",
        slide_number=1,
        text="Deadlock occurs when processes wait indefinitely.",
    )

    assert block.parent_id is None
    assert block.block_type == "text"


def test_slide_blocks_have_independent_metadata():
    block1 = SlideBlock(
        id="block-1",
        slide_number=1,
        text="Definition of deadlock",
    )

    block2 = SlideBlock(
        id="block-2",
        slide_number=1,
        text="Example of deadlock",
    )

    block1.metadata["category"] = "definition"

    assert block1.metadata["category"] == "definition"
    assert block2.metadata == {}
