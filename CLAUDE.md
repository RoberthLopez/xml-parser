# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Run tests:**
```bash
python test_xml_parser.py
```

No build step, linter, or external dependencies — standard library only.

## Architecture

This project has two independent components:

### Python Library (`xml_parser.py`)
- `XMLNode` dataclass: represents a parsed XML element with `tag`, `attributes` (dict), `children` (list), and `text`
  - `.find(tag)` / `.find_all(tag)` traverse the tree
- `XMLParser`: regex tokenizer + stack-based tree builder
  - Single-pass regex (`TOKEN_RE`) matches 6 token types: processing instructions, comments, self-closing tags, opening/closing tags, and text
  - Stack tracks open elements to build parent-child relationships
- Module-level `parse(xml_string) -> XMLNode` convenience wrapper

### Browser UI (`index.html`)
Standalone single-file app (HTML/CSS/JS, no external dependencies). Features: collapsible syntax-highlighted tree, node inspection on click, search/filter, XML formatter, keyboard shortcut `Cmd/Ctrl+Enter` to parse.
