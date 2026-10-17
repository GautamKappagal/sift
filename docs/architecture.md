# Architecture

Sift moves information through these stages:

PDF or PPTX → parsing → SlideBlock → selection → Selection → composing → Note

- `parsing`: extracts content from files
- `selection`: decides which blocks matter
- `composing`: turns selected blocks into notes
- `verification`: checks a note against its sources
- `pyq`: relates material to previous-year questions

All modules communicate through the shared classes in `models.py`.

# Parsing

## What is a block?

A block is the smallest unit of text in a document that can stand alone as a "keep or skip" decision.

A whole slide is too corase, because one slide often mixes an essential definition with a throwaway example.

A line is too fine, because PDFs wrap sentences across lines which would lead the model to judging half-sentences.

Hence, a bullet or paragraph is the sweet spot.

## Defining Block IDs

Format: {deck}-s{slide}-b{index}
Example: os_lec03-s12-b2

Deck is the filename without its extension (Path.stem), loweracsed. This is what keeps IDs unique across decks.

Slide is the 1-based slide or page number, matching what one sees when one opens the file.

Index is the block's 1-based position within that slide, in reading order.

## Warnings
Principle: the parser should never silently drop content it knows it can't read.

Concretely:
- We store warnings as a list in metadata["warnings"], so one block can carry several without redesigning later.
- If a slide has no extractable text but does have an image, we don't skip it. We emit a placeholder block with block_type="image_only", empty text and a warning. That keeps the slide visible in the output, so it shows up later as "partially prcoessed" instead of vanishing.
- For slides that have both text and images, we attach "contains_images" to that slide's blocks.