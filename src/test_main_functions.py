import unittest

from main import *

class TestMainFunctions(unittest.TestCase):

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

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def text_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertNotEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
    
    def text_extract_markdown_links_2(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

if __name__ == "__main__":
    unittest.main()