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

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_text(self):
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        expected_result = [
            TextNode("This is a text node", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD_TEXT), expected_result)

    def test_split_text_2(self):
        node = TextNode("This is a **text** node", TextType.PLAIN_TEXT)
        expected_result = [
            TextNode("This is a ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" node", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD_TEXT), expected_result)

if __name__ == "__main__":
    unittest.main()