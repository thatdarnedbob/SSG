from textnode import *
from htmlnode import *
from blocks import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_nodes = []

    for node in old_nodes:
        split_node = node.text.split(delimiter, maxsplit=2)
        if len(split_node) == 2:
            raise Exception(f"unpaired delimiters in {node}")
        if len(split_node) > 2:
            if len(split_node[0]) > 0:
                text_nodes.append(TextNode(split_node[0], TextType.TEXT))
            if len(split_node[1]) > 1:
                text_nodes.append(TextNode(split_node[1], text_type))
            if len(split_node[2]) > 0:
                temp_node = TextNode(split_node[2], TextType.TEXT)
                text_nodes.extend(split_nodes_delimiter([temp_node], delimiter, text_type))
        if len(split_node) == 1:
            text_nodes.append(node)

    return text_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\]]*)\]\(([^\)]*)\)", text)

def split_nodes_image(old_nodes):
    text_nodes = []

    for node in old_nodes:
        workingtext = node.text
        found_images = extract_markdown_images(workingtext)
        if len(found_images) == 0:
            text_nodes.append(node)
            workingtext = ""
        for image in found_images:
            parts = workingtext.split("![" + image[0] + "](" + image[1] + ")", maxsplit=1)
            if len(parts[0]) > 0:
                text_nodes.append(TextNode(parts[0], TextType.TEXT))
            text_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            workingtext = parts[1]
        if len(workingtext) > 0:
            text_nodes.append(TextNode(workingtext, TextType.TEXT))

    return text_nodes

def split_nodes_link(old_nodes):
    text_nodes = []

    for node in old_nodes:
        # print(f"{node}\n")
        workingtext = node.text
        found_links = extract_markdown_links(workingtext)
        if len(found_links) == 0:
            text_nodes.append(node)
            workingtext = ""
        for link in found_links:
            parts = workingtext.split("[" + link[0] + "](" + link[1] + ")", maxsplit=1)
            if len(parts[0]) > 0:
                text_nodes.append(TextNode(parts[0], TextType.TEXT))
            text_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            workingtext = parts[1]
        if len(workingtext) > 0:
            text_nodes.append(TextNode(workingtext, TextType.TEXT))

    return text_nodes

def text_to_text_nodes(text):
    working_nodes = [TextNode(text, TextType.TEXT)]
    working_nodes = split_nodes_image(working_nodes)
    # practice_nodes = split_nodes_link([TextNode("This is **text** with an _italic_ word and a `code block` and an ", TextType.TEXT, None),
    #                                     TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    #                                     TextNode(" and a [link](https://boot.dev)", TextType.TEXT, None)])'''
    # print(f"\nlen of practice nodes is {len(practice_nodes)}\n")
    working_nodes = split_nodes_link(working_nodes)
    delimiter_pairs = [("**", TextType.BOLD),
                       ("_", TextType.ITALIC),
                       ("`", TextType.CODE)]
    for pair in delimiter_pairs:
        working_nodes = split_nodes_delimiter(working_nodes, pair[0], pair[1])
    return working_nodes

def markdown_to_blocks(md):
    if md is None or md == '':
        return ['']
    
    block_strings = md.split('\n\n')
    formatted_blocks = []
    for block in block_strings:
        block = block.strip()
        if len(block) > 0:
            formatted_blocks.append(block)

    return formatted_blocks

def markdown_to_html_node(markdown):
    working_md = markdown_to_blocks(markdown)
    top_level_parent_node = ParentNode("div", children=[])
    for block in working_md:
        match block_to_block_type(block):
            case BlockType.HEADING:
                top_level_parent_node.children.append(handle_heading(block))
            case BlockType.CODE:
                top_level_parent_node.children.append(handle_code(block))
            case BlockType.QUOTE:
                top_level_parent_node.children.append(handle_quote(block))
            case BlockType.UNORDERED_LIST:
                top_level_parent_node.children.append(handle_unordered_list(block))
            case BlockType.ORDERED_LIST:
                top_level_parent_node.children.append(handle_ordered_list(block))
            case BlockType.PARAGRAPH:
                top_level_parent_node.children.append(handle_paragraph(block))

    return top_level_parent_node

def handle_heading(block):
    split_block = block.split(' ', 1)
    heading_tag = get_heading_tag(split_block[0])
    heading_parent = ParentNode(heading_tag, children=[])
    lines_fixed = ' '.join(split_block[1].splitlines())
    working_text_nodes = text_to_text_nodes(lines_fixed)

    for node in working_text_nodes:
        heading_parent.children.append(text_node_to_html_node(node))

    return heading_parent

def get_heading_tag(prefix):
    return 'h' + str(len(prefix))

def handle_code(block):
    code_block = block.removeprefix('```').removesuffix('```')
    code_leaf = LeafNode(tag=None, value=code_block)
    pre_parent = ParentNode('pre', children=[code_leaf])
    code_parent = ParentNode('code', children=[pre_parent])

    return code_parent

def handle_quote(block):
    quote_parent = ParentNode('blockquote', children=[])
    working_lines = block.splitlines()
    lines_fixed = []
    for line in working_lines:
        lines_fixed.append(line.removeprefix('>').strip())
    lines_fixed = '\n'.join(lines_fixed)
    working_text_nodes = text_to_text_nodes(lines_fixed)

    for node in working_text_nodes:
        quote_parent.children.append(text_node_to_html_node(node))

    return quote_parent

def handle_unordered_list(block):
    unordered_list_parent = ParentNode('ul', children=[])
    individual_lines = block.splitlines()
    for line in individual_lines:
        fixed_line = line.removeprefix('- ')
        working_text_nodes = text_to_text_nodes(fixed_line)
        in_line_parent = ParentNode('li', children=[])
        for node in working_text_nodes:
            in_line_parent.children.append(text_node_to_html_node(node))
        unordered_list_parent.children.append(in_line_parent)
    return unordered_list_parent

def handle_ordered_list(block):
    ordered_list_parent = ParentNode('ol', children=[])
    individual_lines = block.splitlines()
    for line in individual_lines:
        fixed_line = strip_leading_ol_format(line)
        working_text_nodes = text_to_text_nodes(fixed_line)
        in_line_parent = ParentNode('li', children=[])
        for node in working_text_nodes:
            in_line_parent.children.append(text_node_to_html_node(node))
        ordered_list_parent.children.append(in_line_parent)
    return ordered_list_parent

def strip_leading_ol_format(line):
    return line.split(' ', 1)[1]

def handle_paragraph(block):
    paragraph_parent = ParentNode('p', children=[])
    lines_fixed = ' '.join(block.splitlines())
    working_text_nodes = text_to_text_nodes(lines_fixed)

    for node in working_text_nodes:
        paragraph_parent.children.append(text_node_to_html_node(node))

    return paragraph_parent