from textnode import *
from leafnode import LeafNode
from re import findall, MULTILINE, sub
from enum import Enum
from parentnode import ParentNode
from shutil import rmtree, copy
import os

def main():
    copy_static_dir_to_public()

    src = os.path.abspath("content/")
    tmp = os.path.abspath("template.html")
    dst = os.path.abspath("public/")
    generate_pages_recursive(src, tmp, dst)

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
        
'''
This was written with a general idea of what the assignment wanted; I like it, I think it's great. I didn't fully read the assignment.
I think it should support type nesting but I haven't tested it: the course says that's silly. I added a boolean parameter to the function so I could do my thing at the same time, I might make some test cases for my version of the function alongside the ones for the course.
I think this implementation could be wrapped with a different function to call it multiple times, once for each delimiter type, returning a properly tagged set, but I don't yet know how the course plans to use this..
I also want to try and assign the delimeters as values for the TextType Enum. They're currently just numbers because that's how I know to enum, but that could be an easier way to track the delimeters since we don't need to retain an order of the types..
'''
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
    #Decided that matching any number of whitespace ahead of the match was probably unwise; decided to use negative look-behind instead

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

'''
    Oh, cool cool cool. We actually are doing this after all.
    Looking at the split_nodes_delimiter function, I can see clearly that that's not going to support nesting at all.
    Not sure how I managed to think that, it's not injecting HTML tags, we aren't recursing over text, we're breaking things out. I could _try_ and 
    scan ahead in the old_nodes list searching for nodes of plain text that hold a close character, then split on each of those characters and
    convert all the plain text nodes in between to the modified type, but given this format I think I'd need to make combination types, and that'd
    just be too much of a headache. I like the injection method better. I'm not gonna use do_what_the_course_says=False. :,(
'''
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes

#I did a dumb. No deleting list members while looping over that same list.
def markdown_to_blocks(markdown):
    spl = markdown.split("\n\n")
    blocks = []
    for i in range(len(spl)):
        if spl[i]:
            blocks.append(spl[i].strip())
    return blocks

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

def copy_static_dir_to_public(subdir = ""):
    stat_abs = os.path.join(os.path.abspath("static"), subdir)
    pub_abs = os.path.join(os.path.abspath("public"), subdir)

    if not subdir:
        if os.path.exists(pub_abs):
            print("Deleting public folder and all contents...")
            rmtree(pub_abs)
        print("Making public folder...")
        os.mkdir(pub_abs)

    print("In " + stat_abs)
    dir_contents = os.listdir(stat_abs)
    for obj in dir_contents:
        obj_abs_path = os.path.join(stat_abs, obj)
        dst_abs_path = os.path.join(pub_abs, obj)
        if os.path.isfile(obj_abs_path):
            copy(obj_abs_path, dst_abs_path)
            print(f"Copied '{obj_abs_path}' to '{dst_abs_path}'")
        else:
            os.mkdir(dst_abs_path)
            if subdir:
                copy_static_dir_to_public(f"{subdir}/{obj}")
            else:
                copy_static_dir_to_public(obj)

def extract_title(markdown):
    split = markdown.split('\n')
    for line in split:
        match = findall(r"^# (.*)", line)
        if match:
            return match[0].strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r') as f:
            markdown = f.read()
    except FileNotFoundError:
        print(f"File at '{from_path}' not found")
    except PermissionError:
        print(f"File at '{from_path}' could not be opened")
    except Exception:
        print(f"An unexplained error occurred while opening '{from_path}'")

    try:
        with open(template_path, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        print(f"File at '{template_path}' not found")
    except PermissionError:
        print(f"File at '{template_path}' could not be opened")
    except Exception:
        print(f"An unexplained error occurred while opening '{template_path}'")
    
    html_nodes = markdown_to_html_node(markdown)
    html_string = html_nodes.to_html()
    page_title = extract_title(markdown)

    output_string = template.replace("{{ Title }}", page_title).replace("{{ Content }}", html_string)

    try:
        os.makedirs(os.path.dirname(dest_path), 666, True)
        with open(dest_path, 'w') as f:
            f.write(output_string)
    except Exception:
        print(f"An exception occurred while writing to {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_contents = os.listdir(dir_path_content)
    for obj in dir_contents:
        obj_abs_path = os.path.join(dir_path_content, obj)
        dst_abs_path = os.path.join(dest_dir_path, obj)
        if os.path.isfile(obj_abs_path):
            if obj[-3:] == ".md":
                generate_page(obj_abs_path, template_path, (dst_abs_path[:-3] + ".html"))
        else:
            os.mkdir(dst_abs_path)
            generate_pages_recursive(obj_abs_path, template_path, dst_abs_path)

if __name__ == "__main__":
    main()


#Before submitting project: destroy this monolith