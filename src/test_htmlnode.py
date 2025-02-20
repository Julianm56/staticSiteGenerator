from htmlnode import HTMLNode

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
