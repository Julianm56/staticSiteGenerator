from textnode import TextNode, TextType
from delimiter import split_nodes_delimiter  # adjust import path as needed

def test_split_nodes_delimiter():
    # Test 1: Basic split with code
     node = TextNode("Hello `world` today", TextType.NORMAL)
     nodes = split_nodes_delimiter([node], "`", TextType.CODE)
     assert len(nodes) == 3
     assert nodes[0].text == "Hello "
     assert nodes[0].text_type == TextType.NORMAL
     assert nodes[1].text == "world"
     assert nodes[1].text_type == TextType.CODE
     assert nodes[2].text == " today"
     assert nodes[2].text_type == TextType.NORMAL

    # Test 2: Node that isn't TEXT type shouldn't be split
     node = TextNode("Hello `world`", TextType.CODE)
     nodes = split_nodes_delimiter([node], "`", TextType.CODE)
     assert len(nodes) == 1
     assert nodes[0].text == "Hello `world`"
     assert nodes[0].text_type == TextType.CODE

