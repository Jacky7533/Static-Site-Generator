import unittest
from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    
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