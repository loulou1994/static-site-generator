import unittest

# from htmlnode import 
from textnode import TextNode, NODE_TYPE, text_node_to_html_node


class TestTextNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("this is a text node", NODE_TYPE.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "this is a text node")

    def test_img(self):
        node = TextNode("this an image node", NODE_TYPE.IMAGE, "./relative-img.png")
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertIsNotNone(html_node.props)

    def test_none(self):
        node = TextNode("unknown node type", "unknown")
        # html_node = text_node_to_html_node(node)

        self.assertRaises(TypeError, text_node_to_html_node, node)
