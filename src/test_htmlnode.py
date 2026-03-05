import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_members_initialized(self):
        props = {"href": "https://www.google.com", "_target": "_blank"}
        members_data = dict(
            [
                ("tag", "a"),
                ("value", "this is a hyperlink"),
                ("children", None),
                ("props", props),
            ]
        )
        node = HTMLNode(**members_data).__dict__

        self.assertDictEqual(node, members_data)

    def test_propshtml_empty(self):
        node = HTMLNode("")
        props_html = node.props_to_html()

        self.assertEqual(props_html, "")

    def test_propshtml(self):
        props = {"href": "https://www.google.com", "_target": "_blank"}
        node = HTMLNode("a", "this a hyperlink", None, props)
        props_html = f' href="https://www.google.com" _target="_blank"'

        self.assertEqual(node.props_to_html(), props_html)