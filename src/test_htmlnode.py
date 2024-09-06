import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    
    def test_props_to_html_empty(self):
        # Test props_to_html when props is empty
        node = HTMLNode(tag="a")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        # Test props_to_html with one property
        node = HTMLNode(tag="a", props={"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')

    def test_props_to_html_multiple_props(self):
        # Test props_to_html with multiple properties
        node = HTMLNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com" target="_blank"')

    def test_repr_method(self):
        # Test __repr__ method
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.example.com"})
        expected_repr = "HTMLNode(tag=a, value=Click here, children=[], props={'href': 'https://www.example.com'})"
        self.assertEqual(repr(node), expected_repr)

    def test_empty_node(self):
        # Test creation of an empty node
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})

    def test_node_with_children(self):
        # Test node with children
        child1 = HTMLNode(tag="span", value="Child 1")
        child2 = HTMLNode(tag="span", value="Child 2")
        parent = HTMLNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.children, [child1, child2])

    def test_node_with_value(self):
        # Test node with a value
        node = HTMLNode(tag="p", value="This is a paragraph")
        self.assertEqual(node.value, "This is a paragraph")

if __name__ == "__main__":
    unittest.main()