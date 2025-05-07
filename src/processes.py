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

def split_nodes_image(old_nodes):
    text_nodes = []

    for node in old_nodes:
        workingtext = node.text
        found_images = extract_markdown_images(workingtext)
        if len(found_images) == 0:
            text_nodes.append(node)
        for image in found_images:
            parts = workingtext.split("![" + image[0] + "](" + image[1] + ")", maxsplit=1)
            if len(parts[0]) > 0:
                text_nodes.append(TextNode(parts[0], TextType.TEXT))
            text_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            workingtext = parts[1]
        if len(workingtext) > 0:
            text_nodes.append(TextNode[workingtext], TextType.TEXT)

    return text_nodes

def split_nodes_link(old_nodes):
    text_nodes = []

    for node in old_nodes:
        workingtext = node.text
        found_links = extract_markdown_links(workingtext)
        if len(found_links) == 0:
            text_nodes.append(node)
        for link in found_links:
            parts = workingtext.split("[" + link[0] + "](" + link[1] + ")", maxsplit=1)
            if len(parts[0]) > 0:
                text_nodes.append(TextNode(parts[0], TextType.TEXT))
            text_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            workingtext = parts[1]
        if len(workingtext) > 0:
            text_nodes.append(TextNode[workingtext], TextType.TEXT)

    return text_nodes