import re
from textnode import TextNode, NODE_TYPE


def split_node_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != NODE_TYPE.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("The delimiter is not set properly")

        for i in range(len(sections)):
            if sections[i] == "":
                continue

            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], NODE_TYPE.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_image(old_nodes):
    text_nodes = []

    for node in old_nodes:

        if node.text_type != NODE_TYPE.TEXT:
            text_nodes.append(node)
            continue

        if node.text == "":
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            text_nodes.append(node)
            continue

        original_text = node.text
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)

            # print(sections, sep="\n")
            if sections[0] != "":
                text_nodes.append(TextNode(sections[0], NODE_TYPE.TEXT))

            text_nodes.append(TextNode(image[0], NODE_TYPE.IMAGE, image[1]))

            original_text = sections[1]

        if original_text != "":
            text_nodes.append(TextNode(original_text, NODE_TYPE.TEXT))

    return text_nodes


def split_nodes_link(old_nodes):
    text_nodes = []

    for node in old_nodes:

        if node.text_type != NODE_TYPE.TEXT:
            text_nodes.append(node)
            continue

        if node.text == "":
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            text_nodes.append(node)
            continue

        original_text = node.text
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if sections[0] != "":
                text_nodes.append(TextNode(sections[0], NODE_TYPE.TEXT))

            text_nodes.append(TextNode(link[0], NODE_TYPE.LINK, link[1]))

            original_text = sections[1]

        if original_text != "":
            text_nodes.append(TextNode(original_text, NODE_TYPE.TEXT))

    return text_nodes


def text_to_textnode(text):
    node = TextNode(text, NODE_TYPE.TEXT)
    nodes = split_node_delimiter([node], "`", NODE_TYPE.CODE)
    nodes = split_node_delimiter(nodes, "**", NODE_TYPE.BOLD)
    nodes = split_node_delimiter(nodes, "_", NODE_TYPE.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes