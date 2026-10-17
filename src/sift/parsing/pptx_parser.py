from pathlib import Path

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

from sift.models import SlideBlock


def parse_pptx(path: Path) -> list[SlideBlock]:
    """Parse a PPTX file and extract slide blocks.

    Args:
        path (Path): The path to the PPTX file.

    Returns:
        list[SlideBlock]: A list of slide blocks extracted from the PPTX file.
    """
    deck = path.stem.lower()
    blocks = []

    for slide_number, slide in enumerate(Presentation(path).slides, start=1):
        counter = 0
        curr_top_level_block_id = None
        start = len(blocks)  # Store the starting index of blocks for this slide

        # Extract content
        for shape in slide.shapes:
            if shape.has_text_frame:
                if shape == slide.shapes.title:
                    text = shape.text_frame.text.strip()

                    if text:
                        counter += 1
                        block = SlideBlock(
                            id=f"{deck}-s{slide_number}-b{counter}",
                            slide_number=slide_number,
                            text=shape.text_frame.text.strip(),
                            block_type="title"
                        )

                        blocks.append(block)

                else:
                    for paragraph in shape.text_frame.paragraphs:
                        if paragraph.text.strip():
                            counter += 1

                            parent_id = None if paragraph.level == 0 else curr_top_level_block_id
                            block = SlideBlock(
                                id=f"{deck}-s{slide_number}-b{counter}",
                                slide_number=slide_number,
                                text=paragraph.text.strip(),
                                parent_id=parent_id
                            )

                            blocks.append(block)
                            if paragraph.level == 0:
                                curr_top_level_block_id = block.id

        has_image = any(shape.shape_type == MSO_SHAPE_TYPE.PICTURE for shape in slide.shapes)

        if has_image:
            for block in blocks[start:]:  # Iterate over the blocks for this slide
                block.metadata.setdefault("warnings", []).append("contains_images")

    return blocks