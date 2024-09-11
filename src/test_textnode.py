import unittest
from textnode import *


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
    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is an image", text_type_image, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold(self):
        node = TextNode("This is bold", text_type_bold)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

class TestSplitDelimiter(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

class TestExtractMarkdownImages(unittest.TestCase):
    
    def test_single_image(self):
        text = "Here is an image: ![alt text](http://example.com/image.jpg)"
        expected = [("alt text", "http://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_multiple_images(self):
        text = "Two images: ![first](http://example.com/1.jpg) and ![second](http://example.com/2.jpg)"
        expected = [("first", "http://example.com/1.jpg"), ("second", "http://example.com/2.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_no_images(self):
        text = "No images here, just text."
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_special_characters(self):
        text = "Here is an image: ![alt with special chars](http://example.com/img@2x.jpg)"
        expected = [("alt with special chars", "http://example.com/img@2x.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)
    
    def test_image_without_protocol(self):
        text = "![image](www.example.com/image.jpg)"
        expected = [("image", "www.example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_malformed_image(self):
        text = "Malformed image ![alt text(http://example.com/image.jpg)"
        expected = []
        self.assertEqual(extract_markdown_images(text), expected)

class TestExtractMarkdownLinks(unittest.TestCase):
    
    def test_single_link(self):
        text = "Here is a link: [example](http://example.com)"
        expected = [("example", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)
    
    def test_multiple_links(self):
        text = "Two links: [first](http://example.com/1) and [second](http://example.com/2)"
        expected = [("first", "http://example.com/1"), ("second", "http://example.com/2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "No links here, just text."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_special_characters(self):
        text = "Here is a link: [special chars](http://example.com/param?value=1&key=2)"
        expected = [("special chars", "http://example.com/param?value=1&key=2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_without_protocol(self):
        text = "[example](www.example.com)"
        expected = [("example", "www.example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_malformed_link(self):
        text = "Malformed link [example(http://example.com)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

class TestSplitNodesImage(unittest.TestCase):

    def test_split_nodes_image_no_images(self):
        old_nodes = [TextNode("This is a text without images.", text_type_text)]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, old_nodes, "The node should be returned as-is when no images are found.")

    def test_split_nodes_image_one_image(self):
            old_nodes = [TextNode("Here is an image: ![alt](http://url.com)", text_type_text)]
            result = split_nodes_image(old_nodes)
            expected = [
                TextNode("Here is an image: ", text_type_text),
                TextNode("alt", text_type_image, url="http://url.com")
            ]
            self.assertEqual(result, expected, "The node should be split correctly when one image is found.")

    def test_split_nodes_image_multiple_images(self):
        old_nodes = [TextNode("First ![image1](url1) and then ![image2](url2).", text_type_text)]
        result = split_nodes_image(old_nodes)
        expected = [
            TextNode("First ", text_type_text),
            TextNode("image1", text_type_image, url="url1"),
            TextNode(" and then ", text_type_text),
            TextNode("image2", text_type_image, url="url2"),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(result, expected, "The node should be split correctly when multiple images are found.")

    def test_split_nodes_image_malformed_markdown(self):
        old_nodes = [TextNode("Malformed image ![alt text](url without closing parenthesis", text_type_text)]
        result = split_nodes_image(old_nodes)
        self.assertEqual(result, old_nodes, "The node should be returned as-is when the markdown is malformed.")

class TestSplitNodesLink(unittest.TestCase):

    def test_split_nodes_link_no_links(self):
        old_nodes = [TextNode("This is a text without links.", text_type_text)]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, old_nodes, "The node should be returned as-is when no links are found.")

    def test_split_nodes_link_one_link(self):
        old_nodes = [TextNode("Here is a link: [example](http://example.com)", text_type_text)]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("Here is a link: ", text_type_text),
            TextNode("example", text_type_link, url="http://example.com")
        ]
        self.assertEqual(result, expected, "The node should be split correctly when one link is found.")

    def test_split_nodes_link_multiple_links(self):
        old_nodes = [TextNode("First [link1](url1) and then [link2](url2).", text_type_text)]
        result = split_nodes_link(old_nodes)
        expected = [
            TextNode("First ", text_type_text),
            TextNode("link1", text_type_link, url="url1"),
            TextNode(" and then ", text_type_text),
            TextNode("link2", text_type_link, url="url2"),
            TextNode(".", text_type_text)
        ]
        self.assertEqual(result, expected, "The node should be split correctly when multiple links are found.")

    def test_split_nodes_link_malformed_markdown(self):
        old_nodes = [TextNode("Malformed link [example](url without closing parenthesis", text_type_text)]
        result = split_nodes_link(old_nodes)
        self.assertEqual(result, old_nodes, "The node should be returned as-is when the markdown is malformed.")

class TestTextToTextNodes(unittest.TestCase):

    def assertEqualTextNodes(self, result, expected):
        self.assertEqual(result, expected, "The output does not match the expected result.")

    def simple_test(self):
        test_input = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev")
        ]
        result = text_to_textnodes(test_input)
        self.assertEqualTextNodes(result, expected)

    def test_bold_text(self):
        input_text = "This is **bold** text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text.", text_type_text)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqualTextNodes(result, expected)

    def test_italic_text(self):
        input_text = "This is *italic* text."
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" text.", text_type_text)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqualTextNodes(result, expected)

    def test_code_block(self):
        input_text = "This is a `code block`."
        expected = [
            TextNode("This is a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(".", text_type_text)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqualTextNodes(result, expected)

    def test_image(self):
        input_text = "This is an ![alt text](https://example.com/image.jpg) in the text."
        expected = [
            TextNode("This is an ", text_type_text),
            TextNode("alt text", text_type_image, "https://example.com/image.jpg"),
            TextNode(" in the text.", text_type_text)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqualTextNodes(result, expected)

    def test_link(self):
        input_text = "This is a [link](https://example.com) in the text."
        expected = [
            TextNode("This is a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(" in the text.", text_type_text)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqualTextNodes(result, expected)

    def test_multiple_types(self):
        input_text = "Here is **bold**, *italic*, and `code`, with an ![image](https://example.com/img.jpg) and a [link](https://example.com)."
        expected = [
            TextNode("Here is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(", ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(", and ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(", with an ", text_type_text),
            TextNode("image", text_type_image, "https://example.com/img.jpg"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://example.com"),
            TextNode(".", text_type_text)
        ]
        result = text_to_textnodes(input_text)
        self.assertEqualTextNodes(result, expected)


if __name__ == "__main__":
    unittest.main()