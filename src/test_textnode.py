import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node
from textnode import extract_markdown_links, extract_markdown_images

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



if __name__ == "__main__":
    unittest.main()
