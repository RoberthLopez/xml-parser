from xml_parser import parse


def test_basic():
    root = parse("<root><child>hello</child></root>")
    assert root.tag == "root"
    assert root.children[0].tag == "child"
    assert root.children[0].text.strip() == "hello"


def test_attributes():
    root = parse('<book id="1" title="Python"></book>')
    assert root.attributes["id"] == "1"
    assert root.attributes["title"] == "Python"


def test_self_closing():
    root = parse('<root><img src="pic.png"/></root>')
    img = root.find("img")
    assert img is not None
    assert img.attributes["src"] == "pic.png"


def test_nested():
    xml = """
    <library>
        <book id="1"><title>Clean Code</title><author>Martin</author></book>
        <book id="2"><title>SICP</title><author>Abelson</author></book>
    </library>
    """
    root = parse(xml)
    books = root.find_all("book")
    assert len(books) == 2
    assert books[0].find("title").text.strip() == "Clean Code"
    assert books[1].attributes["id"] == "2"


def test_comment_and_pi():
    xml = '<?xml version="1.0"?><!-- comment --><root/>'
    root = parse(xml)
    assert root.tag == "root"


if __name__ == "__main__":
    import traceback
    tests = [test_basic, test_attributes, test_self_closing, test_nested, test_comment_and_pi]
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            traceback.print_exc()
