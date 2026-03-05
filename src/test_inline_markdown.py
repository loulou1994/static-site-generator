import unittest

from textnode import TextNode, NODE_TYPE
from inline_markdown import (
    split_node_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnode,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_bold_delimiter(self):
        text_list = [
            "here's test n° **01**",
            "no boldness after",
            "here we **GO AGAIN**",
        ]
        nodes = []

        for text in text_list:
            nodes.append(TextNode(text, NODE_TYPE.TEXT))

        parsed_nodes = split_node_delimiter(nodes, "**", NODE_TYPE.BOLD)
        bold_nodes_count = 0

        for node in parsed_nodes:
            if node.text_type == NODE_TYPE.BOLD:
                bold_nodes_count += 1

        self.assertEqual(2, 2)

    def test_italic_delimeter(self):
        text_list = ["here's test n° _01_", "no boldness after", "here we _GO AGAIN_"]
        nodes = []

        for text in text_list:
            nodes.append(TextNode(text, NODE_TYPE.TEXT))

        parsed_nodes = split_node_delimiter(nodes, "_", NODE_TYPE.ITALIC)
        italic_nodes_count = 0

        for node in parsed_nodes:
            if node.text_type == NODE_TYPE.ITALIC:
                italic_nodes_count += 1

        self.assertEqual(italic_nodes_count, 2)

    def test_invalid_text(self):
        text_list = ["here's test n° _01_", "no _boldness after", "here we _GO AGAIN_"]
        nodes = []

        for text in text_list:
            nodes.append(TextNode(text, NODE_TYPE.TEXT))

        self.assertRaises(
            ValueError, split_node_delimiter, nodes, "_", NODE_TYPE.ITALIC
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        print(matches)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )

        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            NODE_TYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", NODE_TYPE.TEXT),
                TextNode("image", NODE_TYPE.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            NODE_TYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", NODE_TYPE.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            NODE_TYPE.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", NODE_TYPE.TEXT),
                TextNode("image", NODE_TYPE.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", NODE_TYPE.TEXT),
                TextNode(
                    "second image", NODE_TYPE.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            NODE_TYPE.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", NODE_TYPE.TEXT),
                TextNode("link", NODE_TYPE.LINK, "https://boot.dev"),
                TextNode(" and ", NODE_TYPE.TEXT),
                TextNode("another link", NODE_TYPE.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", NODE_TYPE.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        raw_text_md = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnode(raw_text_md)

        self.assertListEqual(
            [
                TextNode("This is ", NODE_TYPE.TEXT),
                TextNode("text", NODE_TYPE.BOLD),
                TextNode(" with an ", NODE_TYPE.TEXT),
                TextNode("italic", NODE_TYPE.ITALIC),
                TextNode(" word and a ", NODE_TYPE.TEXT),
                TextNode("code block", NODE_TYPE.CODE),
                TextNode(" and an ", NODE_TYPE.TEXT),
                TextNode(
                    "obi wan image", NODE_TYPE.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", NODE_TYPE.TEXT),
                TextNode("link", NODE_TYPE.LINK, "https://boot.dev"),
            ],
            nodes,
        )
