from enum import Enum
class TextType(Enum):
    PLAIN_TEXT = 0
    BOLD_TEXT = 1
    ITALIC_TEXT = 2
    CODE = 3
    LINK = 4
    IMAGE = 5

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"