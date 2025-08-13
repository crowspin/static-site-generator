import unittest

from textnode import TextNode, TextType
from main import text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    
    def test_eq_2(self):
        node = TextNode("This is a test", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_3(self):
        node = TextNode("This is a test", TextType.CODE)
        node2 = TextNode("This is a test", TextType.CODE, "url go heer")
        self.assertNotEqual(node, node2)

    def test_eq_4(self):
        node = TextNode("This is a test", TextType.CODE, "url go heer")
        node2 = TextNode("This is a test", TextType.CODE, "url go heer")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()