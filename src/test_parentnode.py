import unittest

from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("grandchild", "b")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_child(self):
        node = ParentNode("div", None)
        
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_no_parenttag(self):
        child_node = LeafNode("child", "span")
        parent_node = ParentNode(None, [child_node])

        self.assertRaises(ValueError, parent_node.to_html)