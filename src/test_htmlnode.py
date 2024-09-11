import unittest
from htmlnode import *


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

class TestLeafNode(unittest.TestCase):
    
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
    
class TestParentNode(unittest.TestCase):

    # 1. No Tag Provided (Raises ValueError)
    def test_no_tag_provided(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag=None, children=[LeafNode("p", "Test")])
            node.to_html()  # This line is important to trigger the error
        self.assertEqual(str(context.exception), "Tag is required for ParentNode")


    # 2. No Children Provided (Raises ValueError)
    def test_no_children_provided(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag="div", children=None)
            node.to_html()
        self.assertEqual(str(context.exception), "Children are required for ParentNode")

    # 3. Empty Children List (Raises ValueError)
    def test_empty_children(self):
        with self.assertRaises(ValueError) as context:
            node = ParentNode(tag="div", children=[])
            node.to_html()  # This line is important to trigger the error
        self.assertEqual(str(context.exception), "Children are required for ParentNode")

    # 4. Valid ParentNode with One Child (Returns Correct HTML)
    def test_valid_parent_one_child(self):
        child = LeafNode("p", "This is a paragraph.")
        parent = ParentNode(tag="div", children=[child])
        expected_html = "<div><p>This is a paragraph.</p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    # 5. Valid ParentNode with Multiple Children (Returns Correct HTML)
    def test_valid_parent_multiple_children(self):
        child1 = LeafNode("p", "Paragraph 1.")
        child2 = LeafNode("p", "Paragraph 2.")
        parent = ParentNode(tag="div", children=[child1, child2])
        expected_html = "<div><p>Paragraph 1.</p><p>Paragraph 2.</p></div>"
        self.assertEqual(parent.to_html(), expected_html)

    # 6. ParentNode with Properties (Returns Correct HTML with Props)
    def test_parent_with_props(self):
        child = LeafNode("p", "Styled paragraph.")
        parent = ParentNode(tag="div", children=[child], props={"class": "container"})
        expected_html = '<div class="container"><p>Styled paragraph.</p></div>'
        self.assertEqual(parent.to_html(), expected_html)

    # 7. Deeply Nested ParentNode (Recursion Test)
    def test_deeply_nested_parent(self):
        inner_child = LeafNode("span", "Inner text")
        child = ParentNode(tag="p", children=[inner_child])
        parent = ParentNode(tag="div", children=[child])
        expected_html = "<div><p><span>Inner text</span></p></div>"
        self.assertEqual(parent.to_html(), expected_html)
    
    # 8. Valid ParentNode with Nested Children
    def test_valid_parent_with_children(self):
        child1 = LeafNode("p", "First child")
        child2 = LeafNode("p", "Second child")
        node = ParentNode(tag="div", children=[child1, child2])
        expected_html = "<div><p>First child</p><p>Second child</p></div>"
        self.assertEqual(node.to_html(), expected_html)
    
    # 9. ParentNOde with Attribute (props)
    def test_parent_with_props(self):
        child = LeafNode("p", "Example text")
        node = ParentNode(tag="div", children=[child], props={"class": "container"})
        expected_html = '<div class="container"><p>Example text</p></div>'
        self.assertEqual(node.to_html(), expected_html)

    # 10. ParentNode with No Tag
    def test_no_tag_provided(self):
        child = LeafNode("p", "Test")
        node = ParentNode(tag=None, children=[child])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Tag is required for ParentNode")
    
    # 11. ParentNode with Empty Props
    def test_parent_with_empty_props(self):
        child = LeafNode("p", "Test")
        node = ParentNode(tag="div", children=[child], props={})
        expected_html = "<div><p>Test</p></div>"
        self.assertEqual(node.to_html(), expected_html)

    # 12. ParentNode with Multiple Levels of Nesting
    def test_nested_parent_nodes(self):
        inner_child = LeafNode("span", "Inner child")
        outer_child = ParentNode(tag="div", children=[inner_child])
        node = ParentNode(tag="section", children=[outer_child])
        expected_html = "<section><div><span>Inner child</span></div></section>"
        self.assertEqual(node.to_html(), expected_html)
    
    # 13. ParentNode with Empty String as Tag
    def test_empty_string_tag(self):
        child = LeafNode("p", "Test")
        node = ParentNode(tag="", children=[child])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Tag is required for ParentNode")
    
    # 14. ParentNode with Single Child
    def test_parent_with_single_child(self):
        child = LeafNode("p", "Single child")
        node = ParentNode(tag="div", children=[child])
        expected_html = "<div><p>Single child</p></div>"
        self.assertEqual(node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()