from enum import Enum

from htmlnode import LeafNode


class NODE_TYPE(Enum):
    CODE = "code"
    LINK = "link"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    IMAGE = "image"


class TextNode:

    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value: object) -> bool:
        current_object = self.__dict__
        object_to_compare = value.__dict__

        for key in current_object:
            if current_object[key] != object_to_compare[key]:
                return False

        return True

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case NODE_TYPE.TEXT:
            return LeafNode(text_node.text)

        case NODE_TYPE.BOLD:
            return LeafNode(text_node.text, "b")

        case NODE_TYPE.ITALIC:
            return LeafNode(text_node.text, "i")

        case NODE_TYPE.IMAGE:
            return LeafNode(text_node.text, "img", {"src": text_node.url})

        case NODE_TYPE.CODE:
            return LeafNode(text_node.text, "code")

        case NODE_TYPE.LINK:
            return LeafNode(
                text_node.text, "a", {"href": text_node.url, "alt": text_node.text}
            )

        case _:
            raise TypeError("Invalid text node")
