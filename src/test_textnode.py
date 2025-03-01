import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node
from textnode import extract_markdown_links, extract_markdown_images, split_nodes_link, split_nodes_image, text_to_textnodes, split_nodes_delimiter
from textnode import markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def url_eq_none(self):
        node = TextNode("Test",TextType.BOLD)
        self.assertEqual(node.url, None)

    def text_type_diff(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertNotEqual(node,node2)


import unittest

class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text(self):
        text_node = TextNode(text_type=TextType.NORMAL, text="Hello world")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello world")
        self.assertEqual(html_node.props, {})

    def test_bold(self):
        text_node = TextNode(text_type=TextType.BOLD, text="Bold text")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.props, {})



class TestExtraction(unittest.TestCase):

    def test_extract_markdown_images(self):
      # Test single image
      text = "This is ![my image](https://example.com/img.png)"
      matches = extract_markdown_images(text)
      self.assertListEqual([("my image", "https://example.com/img.png")], matches)

    # Test multiple images
      text = "![img1](url1.png) and ![img2](url2.png)"
      matches = extract_markdown_images(text)
      self.assertListEqual([("img1", "url1.png"), ("img2", "url2.png")], matches)

    def test_extract_markdown_links(self):
    # Test single link
     text = "Here is a [link](https://boot.dev)"
     matches = extract_markdown_links(text)
     self.assertListEqual([("link", "https://boot.dev")], matches)

    # Test that images aren't matched as links
     text = "![not a link](https://example.com/img.png)"
     matches = extract_markdown_links(text)
     self.assertListEqual([], matches)


class TestMarkdownSplitter(unittest.TestCase):
    def test_split_images(self):
        # This is the test provided in the assignment
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_images_no_images(self):
        # Test with no images
        node = TextNode("This is text with no images", TextType.NORMAL)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)
    
    def test_split_images_with_non_text_node(self):
        # Test with a non-TEXT node
        node = TextNode("image", TextType.IMAGES, "https://example.com/image.jpg")
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)


    def test_split_links(self):
      # Test basic link splitting
      node = TextNode(
        "This is text with a [link to Boot.dev](https://www.boot.dev) and [another link](https://example.com)",
        TextType.NORMAL,
       )
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.NORMAL),
            TextNode("link to Boot.dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("another link", TextType.LINKS, "https://example.com"),
        ],
        new_nodes,
      )

    def test_split_links_no_links(self):
      # Test with no links
      node = TextNode("This is text with no links", TextType.NORMAL)
      new_nodes = split_nodes_link([node])
      self.assertListEqual([node], new_nodes)

    def test_split_links_with_non_text_node(self):
      # Test with a non-TEXT node
      node = TextNode("link text", TextType.LINKS, "https://example.com")
      new_nodes = split_nodes_link([node])
      self.assertListEqual([node], new_nodes)

    def test_split_links_empty_text(self):
      # Test with a link at the beginning
      node = TextNode("[link text](https://example.com) followed by text", TextType.NORMAL)
      new_nodes = split_nodes_link([node])
      self.assertListEqual(
        [
            TextNode("link text", TextType.LINKS, "https://example.com"),
            TextNode(" followed by text", TextType.NORMAL),
        ],
        new_nodes,
      )

class Test_text_to_textnode(unittest.TestCase):
    def test_text_to_textnodes_with_bold(self):
     text = "This is **bold** text"
     expected = [
        TextNode("This is ", TextType.NORMAL),
        TextNode("bold", TextType.BOLD),
        TextNode(" text", TextType.NORMAL)
     ]
     actual = text_to_textnodes(text)
     assert actual == expected, f"Expected {expected}, got {actual}"

    def test_text_to_textnodes_with_italic(self):
        text = "This is _italic_ text"
        expected = [
        TextNode("This is ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" text", TextType.NORMAL)
        ]
        actual = text_to_textnodes(text)
        assert actual == expected, f"Expected {expected}, got {actual}"

    def test_text_to_textnodes_with_code(self):
        text = "This is `code` text"
        expected = [
        TextNode("This is ", TextType.NORMAL),
        TextNode("code", TextType.CODE),
        TextNode(" text", TextType.NORMAL)
        ]
        actual = text_to_textnodes(text)
        assert actual == expected, f"Expected {expected}, got {actual}"

    def test_text_to_textnodes_with_link(self):
        text = "This is a [link](https://boot.dev) text"
        expected = [
        TextNode("This is a ", TextType.NORMAL),
        TextNode("link", TextType.LINKS, "https://boot.dev"),
        TextNode(" text", TextType.NORMAL)
        ]
        actual = text_to_textnodes(text)
        assert actual == expected, f"Expected {expected}, got {actual}"
class test_delimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
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

def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )
if __name__ == "__main__":
    unittest.main()
