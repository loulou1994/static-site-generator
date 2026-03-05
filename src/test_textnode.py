import unittest
from textnode import TextNode, NODE_TYPE


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a test node", NODE_TYPE.BOLD)
        node2 = TextNode("This is a test node", NODE_TYPE.BOLD)

        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("This is a test node", NODE_TYPE.BOLD)
        node2 = TextNode("This is a test node", NODE_TYPE.CODE)

        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a test node", NODE_TYPE.BOLD)

        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()
