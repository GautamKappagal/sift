from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SlideBlock:
    """One block of content (a title, bullet, line of text or image) on one slide or page.

    Attributes:
        id: The unique identifier of the slide block.
        slide_number: The number of the slide in the presentation.
        text: The text content of the slide block.
        block_type: The type of the slide block (default is "text").
        parent_id: The unique identifier of the parent slide block (if any).
        metadata: Additional metadata associated with the slide block.
    """

    id: str
    slide_number: int
    text: str
    block_type: str = "text"
    parent_id: str | None = None
    metadata: dict = field(default_factory=dict)


@dataclass
class Selection:
    """A selection of slide blocks in a presentation.

    Attributes:
        block_id: The unique identifier of the selected slide block.
        keep_probability: The probability of keeping the selected slide block.
        model_version: The version of the model used for selection.
    """

    block_id: str
    keep_probability: float
    model_version: str


@dataclass
class Note:
    """A note associated with a slide block in a presentation.

    Attributes:
        text: The text content of the note.
        source_block_ids: A list of unique identifiers of the slide blocks that the note is associated with.
    """

    text: str
    source_block_ids: list[str] = field(default_factory=list)
