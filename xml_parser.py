"""A simple XML parser that builds a tree of nodes."""

import re
from dataclasses import dataclass, field


@dataclass
class XMLNode:
    tag: str
    attributes: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    text: str = ""

    def find(self, tag):
        """Return first child with matching tag."""
        for child in self.children:
            if child.tag == tag:
                return child
        return None

    def find_all(self, tag):
        """Return all children with matching tag."""
        return [child for child in self.children if child.tag == tag]

    def __repr__(self, indent=0):
        pad = "  " * indent
        attrs = "".join(f' {k}="{v}"' for k, v in self.attributes.items())
        lines = [f"{pad}<{self.tag}{attrs}>"]
        if self.text.strip():
            lines.append(f"{pad}  {self.text.strip()}")
        for child in self.children:
            lines.append(child.__repr__(indent + 1))
        lines.append(f"{pad}</{self.tag}>")
        return "\n".join(lines)


class XMLParser:
    # Matches: opening tags, closing tags, self-closing tags, text content
    TOKEN_RE = re.compile(
        r"<\?.*?\?>|"                          # processing instructions (skip)
        r"<!--.*?-->|"                         # comments (skip)
        r"<([a-zA-Z_][\w.-]*)([^>]*?)/>|"     # self-closing tag
        r"<([a-zA-Z_][\w.-]*)([^>]*)>|"       # opening tag
        r"</([a-zA-Z_][\w.-]*)>|"             # closing tag
        r"([^<]+)",                            # text
        re.DOTALL,
    )
    ATTR_RE = re.compile(r'([\w.-]+)\s*=\s*(?:"([^"]*?)"|\'([^\']*?)\')')

    def parse(self, xml: str) -> XMLNode:
        tokens = self.TOKEN_RE.finditer(xml)
        stack = []
        root = None

        for m in tokens:
            sc_tag, sc_attrs, op_tag, op_attrs, cl_tag, text = m.groups()

            if sc_tag:  # self-closing
                node = XMLNode(sc_tag, self._parse_attrs(sc_attrs))
                self._attach(stack, node)
                if root is None:
                    root = node

            elif op_tag:  # opening tag
                node = XMLNode(op_tag, self._parse_attrs(op_attrs))
                self._attach(stack, node)
                stack.append(node)
                if root is None:
                    root = node

            elif cl_tag:  # closing tag
                if stack and stack[-1].tag == cl_tag:
                    stack.pop()

            elif text:
                content = text.strip()
                if content and stack:
                    stack[-1].text += text

        if root is None:
            raise ValueError("No root element found")
        return root

    def _parse_attrs(self, raw: str) -> dict:
        return {
            k: v2 if v2 is not None else v3
            for k, v2, v3 in self.ATTR_RE.findall(raw or "")
        }

    def _attach(self, stack, node):
        if stack:
            stack[-1].children.append(node)


def parse(xml: str) -> XMLNode:
    return XMLParser().parse(xml)
