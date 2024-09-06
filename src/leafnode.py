from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("Value is required for LeafNode")
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required for LeafNode")
        
        if self.tag is None:
            return self.value
        
        props_str = self.props_to_html()  # Ensure props_to_html() is called as a method
        if props_str:
            return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        

