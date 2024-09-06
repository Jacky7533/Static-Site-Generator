class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = str(tag) if tag is not None else None
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        # Add a leading space and ensure attributes are joined correctly
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"