from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode has no tag")
        if not self.children:
            raise ValueError("ParentNode has no children")
        
        prop_string = ""
        if type(self.props) is dict:
            for p,v in self.props.items():
                prop_string += f" {p}=\"{v}\""

        child_string = ""
        for child in self.children:
            child_string += child.to_html()

        return f"<{self.tag}{prop_string}>{child_string}</{self.tag}>"