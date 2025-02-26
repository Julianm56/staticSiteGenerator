from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

def test_props_to_html():
    # Test case 1: No props
    node = HTMLNode()
    assert node.props_to_html() == ""

    # Test case 2: Single prop
    node = HTMLNode(props={"href": "https://www.google.com"})
    assert node.props_to_html() == ' href="https://www.google.com"'

    # Test case 3: Multiple props
    node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
    assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'



def test_leaf_node_with_tag():
    node = LeafNode("p", "Hello, World!")
    assert node.to_html() == "<p>Hello, World!</p>"

def test_leaf_node_with_props():
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    assert node.to_html() == '<a href="https://www.google.com">Click me!</a>'

def test_leaf_node_without_tag():
    node = LeafNode(None, "Just some text")
    assert node.to_html() == "Just some text"

def test_leaf_node_missing_value():
        LeafNode("p", None).to_html()

def test_simple_parent():
    parent = ParentNode(
        "div",
        [LeafNode("span", "Hello")]
    )
    assert parent.to_html() == "<div><span>Hello</span></div>", "Simple parent test failed"
    print("Simple parent test passed!")

def test_parent_with_props():
    parent = ParentNode(
        "div",
        [LeafNode("p", "Text")],
        {"class": "container"}
    )
    assert parent.to_html() == '<div class="container"><p>Text</p></div>', "Parent with props test failed"
    print("Parent with props test passed!")

def test_multiple_children():
    parent = ParentNode(
        "div",
        [
            LeafNode("p", "First"),
            LeafNode("p", "Second"),
            LeafNode(None, "Plain text")
        ]
    )
    assert parent.to_html() == "<div><p>First</p><p>Second</p>Plain text</div>", "Multiple children test failed"
    print("Multiple children test passed!")

def test_nested_parents():
    parent = ParentNode(
        "div",
        [
            ParentNode(
                "section",
                [LeafNode("p", "Nested text")]
            )
        ]
    )
    assert parent.to_html() == "<div><section><p>Nested text</p></section></div>", "Nested parents test failed"
    print("Nested parents test passed!")

def test_error_cases():
    try:
        bad_parent = ParentNode(None, [LeafNode("p", "Text")])
        bad_parent.to_html()
        assert False, "Should have raised ValueError for None tag"
    except ValueError:
        print("Error case 1 passed!")

    try:
        bad_parent = ParentNode("div", None)
        bad_parent.to_html()
        assert False, "Should have raised ValueError for None children"
    except ValueError:
        print("Error case 2 passed!")
