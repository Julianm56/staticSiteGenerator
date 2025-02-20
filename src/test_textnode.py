import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()
