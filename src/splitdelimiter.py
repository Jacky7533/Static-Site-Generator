from textnode import TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        # If node is not of type 'text', add it as-is
        if node.text_type != "text":
            new_nodes.append(node)
            continue

    # Split the text by delimiter
    split_text = node.text.split(delimiter)

    # Ensure valid delimniter pairs
    if len(split_text) % 2 == 0:
        raise ValueError("Unmatched delimiter found in text.")
    
    for i, part in enumerate(split_text):
        if i % 2 == 0:
            new_nodes.append(TextNode(part, "text")) # Add as text node
        else:
            new_nodes.append(TextNode(part, text_type)) # Add as new text type
    
    return new_nodes