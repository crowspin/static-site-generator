import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world! Me bored.")
        self.assertEqual(node.to_html(), "<b>Hello, world! Me bored.</b>")

if __name__ == "__main__":
    unittest.main()