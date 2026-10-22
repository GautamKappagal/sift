import argparse
from __future__ import annotations

from pathlib import Path

from sift.parsing import parse_document


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="sift")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_cmd = subparsers.add_parser("parse", help="Parse a document into blocks")
    parse_cmd.add_argument("path", type=Path)
    parse_cmd.add_argument("--images", type=Path, default=None)

    args = parser.parse_args(argv)

    if not args.path.is_file():
        raise SystemExit(f"Error: file not found: {args.path}")

    try:
        blocks = parse_document(args.path, image_dir=args.images)
    except ValueError as error:
        raise SystemExit(f"Error: {error}")

    for block in blocks:
        print(f"{block.id:<24} {block.block_type:<6} {block.text[:60]}")

    slides = {block.slide_number for block in blocks}
    print(f"\n{len(blocks)} blocks across {len(slides)} slides")