import unittest
from textnode import TextNode


class TestTextNode(unittest.TestCase):

    def test_eq(self):
        # Test equality with same properties
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node1, node2)

    def test_neq_different_text_type(self):
        # Test inequality when text_type is different
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node1, node2)

    def test_neq_different_text(self):
        # Test inequality when text is different
        node1 = TextNode("This is a text node", "bold")
        node2 = TextNode("Different text", "bold")
        self.assertNotEqual(node1, node2)

    def test_eq_url_none(self):
        # Test equality when url is None for both
        node1 = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", None)
        self.assertEqual(node1, node2)

    def test_eq_with_url(self):
        # Test equality when URL is present
        node1 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertEqual(node1, node2)

    def test_neq_different_url(self):
        # Test inequality when url is different
        node1 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        node2 = TextNode("This is a text node", "bold", "https://www.example.com")
        self.assertNotEqual(node1, node2)

    def test_neq_one_url_none(self):
        # Test inequality when one URL is None and the other is not
        node1 = TextNode("This is a text node", "bold", None)
        node2 = TextNode("This is a text node", "bold", "https://www.boot.dev")
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()