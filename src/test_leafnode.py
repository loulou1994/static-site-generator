import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_tohtml_error(self):
        node = LeafNode(None, "p")

        self.assertRaises(ValueError, node.to_html)
    
    def test_leaf_tohtml_text(self):
        node = LeafNode("here's a plain text")

        self.assertEqual(node.to_html(), "here's a plain text")