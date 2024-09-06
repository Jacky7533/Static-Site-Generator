import unittest
from htmlnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    
#test_leafnode_no_tag: Verifies that LeafNode returns raw text when no tag is provided.
    def test_leafnode_no_tag(self):
        # Test LeafNode with no tag
        node = LeafNode(value="This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")
#test_leafnode_with_tag: Verifies that LeafNode correctly renders HTML with a specified tag.
    def test_leafnode_with_tag(self):
        # Test LeafNode with a tag
        node = LeafNode(tag="p", value="This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")
#test_leafnode_with_props: Tests the to_html method when properties are provided, ensuring they are included in the rendered HTML.
    def test_leafnode_with_props(self):
        # Test LeafNode with tag and props
        node = LeafNode(tag="a", value="Click here", props={"href": "https://www.example.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.example.com">Click here</a>')
#test_leafnode_with_empty_props: Ensures that LeafNode renders HTML correctly even when properties are an empty dictionary.
    def test_leafnode_with_empty_props(self):
        # Test LeafNode with tag but no props
        node = LeafNode(tag="div", value="Content", props={})
        self.assertEqual(node.to_html(), "<div>Content</div>")
#test_leafnode_missing_value: Ensures that initializing a LeafNode without a value raises a ValueError.
    def test_leafnode_missing_value(self):
        # Test LeafNode initialization without a value should raise ValueError
        with self.assertRaises(ValueError):
            node = LeafNode(tag="p", value=None)
            node.to_html()
#test_leafnode_repr: Tests the __repr__ method to ensure it correctly represents the LeafNode object for debugging.
    def test_leafnode_repr(self):
        # Test __repr__ method
        node = LeafNode(tag="span", value="Example")
        expected_repr = "LeafNode(span, Example, {})"
        self.assertEqual(repr(node), expected_repr)
#test_leafnode_value_only: Verifies that LeafNode with only a value and no tag behaves as expected.
    def test_leafnode_value_only(self):
        # Test LeafNode with value only and no tag
        node = LeafNode(value="Just text")
        self.assertEqual(node.to_html(), "Just text")

if __name__ == "__main__":
    unittest.main()