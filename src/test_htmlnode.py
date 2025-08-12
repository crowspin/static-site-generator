import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href":"This is a test"})
        expected = " href=\"This is a test\""
        self.assertEqual(node.props_to_html(), expected)
    
    def test_eq_2(self):
        node = HTMLNode(props={"href":"https://www.google.com", "target": "_blank"})
        expected = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected)

    def test_eq_3(self):
        node = HTMLNode(props={"href":"This is NOT a test", "target": "_blank"})
        expected = " href=\"This is NOT a test\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), expected)

if __name__ == "__main__":
    unittest.main()