from textnode import *
from htmlnode import *
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
    return re.findall(r"\[([^\]]*)\]\(([^\)]*)\)", text)