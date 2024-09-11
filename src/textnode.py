from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):

    # Regular expression to find markdown image syntax: ![alt text](url)
    image_pattern = r"!\[(.*?)\]\((.*?)\)"

    # Use findall to extract all matches of the patterns
    matches = re.findall(image_pattern, text)

    return matches

def extract_markdown_links(text):

    # Regular expressions to find markdown link syntax
    link_pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"

    # Use find all to extract all matches of the patterns
    matches = re.findall(link_pattern,text)

    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        # Extract images and their positions
        images = extract_markdown_images(old_node.text)
        
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Split text based on image patterns
        split_text = re.split(r'!\[(.*?)\]\((.*?)\)', old_node.text)
        
        if len(split_text) % 3 != 1:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        split_nodes = []
        
        for i, part in enumerate(split_text):
            if i % 3 == 0:
                # This is text between images
                if part:
                    split_nodes.append(TextNode(part, text_type_text))
            elif i % 3 == 1:
                # This is the alt text of the image
                image_alt = part
            elif i % 3 == 2:
                # This is the URL of the image
                image_url = part
                split_nodes.append(TextNode(image_alt, text_type_image, url=image_url))
        
        new_nodes.extend(split_nodes)
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        # Extract images and their positions
        links = extract_markdown_links(old_node.text)
        
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Split text based on image patterns
        split_text = re.split(r"(?<!!)\[(.*?)\]\((.*?)\)", old_node.text)
        
        if len(split_text) % 3 != 1:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        split_nodes = []
        
        for i, part in enumerate(split_text):
            if i % 3 == 0:
                # This is text between images
                if part:
                    split_nodes.append(TextNode(part, text_type_text))
            elif i % 3 == 1:
                # This is the alt text of the image
                link_text = part
            elif i % 3 == 2:
                # This is the URL of the image
                link_url = part
                split_nodes.append(TextNode(link_text, text_type_link, url=link_url))
        
        new_nodes.extend(split_nodes)
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes