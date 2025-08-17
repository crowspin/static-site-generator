from re import findall, sub, MULTILINE
from enum import Enum

from parentnode import ParentNode
from textnode import TextNode, TextType
from nodes import text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    paragraph = 0
    heading = 1
    code = 2
    quote = 3
    unordered_list = 4
    ordered_list = 5

def block_to_block_type(block):
    header_match = findall(r"^#{1,6} \w*", block)
    if header_match:
        return BlockType.heading

    if block[:3] == "```" and block[-3:] == "```":
        return BlockType.code
    
    split = block.split("\n")
    quote_test = True
    ul_test = True
    ol_test = True
    for i in range(len(split)):
        if split[i][0] != '>':
            quote_test = False
        if split[i][0:2] != "- ":
            ul_test = False
        ol_match = findall(fr"^{i+1}. ", split[i])
        if not ol_match:
            ol_test = False
    if quote_test:
        return BlockType.quote
    if ul_test:
        return BlockType.unordered_list
    if ol_test:
        return BlockType.ordered_list
    return BlockType.paragraph

def text_block_to_children(block):
    text_nodes = text_to_textnodes(block)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes

def list_block_to_li_children(block):
    html_nodes = []
    matches = findall(r"^(?:\d+\. |- )(.*)$", block, MULTILINE)
    for match in matches:
        html_nodes.append(ParentNode("li", text_block_to_children(match)))
    return html_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.quote:
                block_nodes.append(ParentNode("blockquote", text_block_to_children(sub(r"^>\s*", "", block, flags=MULTILINE).replace("\n", "<br />"))))
            case BlockType.unordered_list:
                block_nodes.append(ParentNode("ul", list_block_to_li_children(block)))
            case BlockType.ordered_list:
                block_nodes.append(ParentNode("ol", list_block_to_li_children(block)))
            case BlockType.code:
                block_nodes.append(ParentNode("pre", [text_node_to_html_node(TextNode(block[3:-3].strip(), TextType.CODE))]))
                #block_nodes.append(ParentNode("code", [ParentNode("pre", [LeafNode(None, block[3:-3])])]))
                continue
            case BlockType.heading:
                match = findall(r"^(#{1,6}) (.*)", block)
                block_nodes.append(ParentNode(f"h{len(match[0][0])}", text_block_to_children(match[0][1])))
                continue
            case _:
                block_nodes.append(ParentNode("p", text_block_to_children(block)))
    root_node = ParentNode("div", block_nodes)
    return root_node

def markdown_to_blocks(markdown):
    spl = markdown.split("\n\n")
    blocks = []
    for i in range(len(spl)):
        if spl[i]:
            blocks.append(spl[i].strip())
    return blocks

def extract_title(markdown):
    split = markdown.split('\n')
    for line in split:
        match = findall(r"^# (.*)", line)
        if match:
            return match[0].strip()