from textnode import *
from leafnode import LeafNode

def main():
    tn = TextNode("This is some anchor text", TextType.LINK)
    print(tn)

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Invalid TextType for conversion to HTML LeafNode.")

main()