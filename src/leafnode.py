from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode has no Value")
        if not self.tag:
            return self.value
        
        built_string = f"<{self.tag}"
        if type(self.props) is dict:
            for p,v in self.props.items():
                built_string += f" {p}=\"{v}\""
        built_string += f">{self.value}</{self.tag}>"

        return built_string