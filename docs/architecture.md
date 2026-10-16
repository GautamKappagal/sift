# Architecture

Sift moves information through these stages:

PDF or PPTX → parsing → SlideBlock → selection → Selection → composing → Note

- `parsing`: extracts content from files
- `selection`: decides which blocks matter
- `composing`: turns selected blocks into notes
- `verification`: checks a note against its sources
- `pyq`: relates material to previous-year questions

All modules communicate through the shared classes in `models.py`.