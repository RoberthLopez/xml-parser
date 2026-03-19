# xml-parser

A simple XML parser with an interactive browser-based UI.

## Files

- **`xml_parser.py`** — Python parser library
- **`index.html`** — standalone browser UI (no dependencies, no build step)
- **`test_xml_parser.py`** — test suite for the Python parser

## Python Usage

```python
from xml_parser import parse

root = parse("<root><child id='1'>hello</child></root>")

root.tag                        # "root"
root.find("child")              # first <child> node
root.find("child").text.strip() # "hello"
root.find("child").attributes   # {"id": "1"}
root.find_all("child")          # list of all <child> nodes
```

### XMLNode API

| Method / Property | Description |
|---|---|
| `.tag` | Element tag name |
| `.attributes` | Dict of attribute key/value pairs |
| `.children` | List of child `XMLNode` objects |
| `.text` | Text content of the element |
| `.find(tag)` | First child matching `tag`, or `None` |
| `.find_all(tag)` | All children matching `tag` |

## Browser UI

Open `index.html` directly in any browser — no server needed.

**Features:**
- Syntax-highlighted collapsible tree
- Click any node to inspect its attributes and text
- Search bar to filter and highlight matching nodes
- Format button to auto-indent XML
- Node count and tree depth in the status bar
- `⌘ Enter` / `Ctrl Enter` to parse

## Running Tests

```bash
python test_xml_parser.py
```
