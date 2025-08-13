from textnode import *
from leafnode import LeafNode

def main():
    #tn = TextNode("This is some anchor text", TextType.LINK)
    #print(tn)
    pass

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

main()