# Architecture

Sift moves information through these stages:

PDF or PPTX (more formats later) → parsing → SlideBlock → selection → Selection → composing → Note

- `parsing`: extracts content from files
- `selection`: decides which blocks matter
- `composing`: turns selected blocks into notes
- `verification`: checks a note against its sources
- `pyq`: relates material to previous-year questions

All modules communicate through the shared classes in `models.py`.

# Parsing

Callers never check what format a file is. They call `parse_document(path, image_dir)`, which picks the right parser from the file extension and raises `ValueError` for unsupported types. Each parser lives in `parsing/` and is named `<format>_parser.py`. Adding a format means writing one parser and adding one line to the `PARSERS` dictionary.

## What is a block?

A block is the smallest unit of content in a document that can stand alone as a "keep or skip" decision.

A whole slide is too coarse, because one slide often mixes an essential definition with a throwaway example.

A line is too fine, because PDFs wrap sentences across lines, which would lead the model to judge half-sentences.

A bullet or paragraph is the sweet spot. Images are blocks too.

Block types: `title`, `text` (the default) and `image`.

## Block IDs

Format: `{deck}-s{slide}-b{index}`
Example: `os_lec03-s12-b2`

- Deck is the filename without its extension (`Path.stem`), lowercased. This keeps IDs unique across decks.
- Slide is the 1-based slide or page number, matching what you see when you open the file.
- Index is the block's 1-based position within that slide. Text and images share one numbering and restart on every slide.

IDs must stay stable: hand labels will refer to them, so changing the splitting rules after labeling starts can silently break the labels.

## Hierarchy

In PPTX, a paragraph at indent level 1 or deeper gets the most recent level-0 block on the same slide as its `parent_id`. Titles are never parents. This is what lets the selector later keep a whole group together.

## Images

The parser never silently drops content it cannot read. Every embedded image becomes a block with `block_type="image"` and empty text. If an `image_dir` is given, the image file is saved there, named after the block ID, and its location is stored in `metadata["image_path"]`. A slide that