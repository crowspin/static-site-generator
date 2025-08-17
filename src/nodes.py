from re import findall

from textnode import TextNode, TextType
from leafnode import LeafNode

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
            return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Invalid TextType for conversion to HTML LeafNode.")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type, do_what_the_course_says=True):
    new_nodes = []
    for node in old_nodes:

        if do_what_the_course_says and node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        if delimiter in node.text:
            spl = node.text.split(delimiter)

            if len(spl) % 2 != 1:
                if do_what_the_course_says:
                    raise Exception(f"Invalid markdown syntax: {node} does not exclusively contain matched sets of {delimiter} delimiters")
                else:
                    spl[-2] = spl[-2] + delimiter + spl[-1]
                    del spl[-1]
            
            for i in range(len(spl)):
                if spl[i]:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(spl[i], node.text_type))
                    else:
                        new_nodes.append(TextNode(spl[i], text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    return findall(r"\!\[(.*?)\]\(([\w:\/.]+)\)", text)

def extract_markdown_links(text):
    return findall(r"(?<!!)\[(.*?)\]\((.+?)\)", text)

def split_nodes_link_or_image(use_case, old_nodes):
    if use_case is TextType.LINK:
        extract_func = extract_markdown_links
        splitter = ""
    elif use_case is TextType.IMAGE:
        extract_func = extract_markdown_images
        splitter = "!"
    else: 
        raise TypeError("Use case must be LINK or IMAGE")
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        matches = extract_func(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        op_text = node.text
        for match in matches:
            spl = op_text.split(splitter + f"[{match[0]}]({match[1]})", 1)
            if spl[0]:
                new_nodes.append(TextNode(spl[0], TextType.PLAIN_TEXT))
            new_nodes.append(TextNode(match[0], use_case, match[1]))
            op_text = spl[1]
        if op_text:
            new_nodes.append(TextNode(op_text, TextType.PLAIN_TEXT))

    return new_nodes

def split_nodes_image(old_nodes):
    return split_nodes_link_or_image(TextType.IMAGE, old_nodes)

def split_nodes_link(old_nodes):
    return split_nodes_link_or_image(TextType.LINK, old_nodes)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes
