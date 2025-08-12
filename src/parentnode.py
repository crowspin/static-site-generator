from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode has no tag")
        if not self.children:
            raise ValueError("ParentNode has no children")
        built_string = ""
        for child in self.children:
            built_string += child.to_html()
        return f"<{self.tag}>{built_string}</{self.tag}>"