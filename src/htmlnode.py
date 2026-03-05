class HTMLNode:
    def __init__(self, tag="", value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""

        node_props = []

        for key, value in self.props.items():
            node_props.append(f'{key}="{value}"')

        return f" {" ".join(node_props)}"

    def __repr__(self):
        return f"""
            HTMLNode(
                tag={self.tag}
                value={self.value}
                children={self.children}
                props={self.props}
            )
        """


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("The value member shouldn't be empty")

        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"""
            LeafNode(
                tag={self.tag}
                value={self.value}
                props={self.props}
            )
        """


class ParentNode(HTMLNode):    
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("The tag member is missing")

        if self.children is None or not len(self.children):
            raise ValueError("The children member is missing")

        children_nodes = []
        for child in self.children:
            children_nodes.append(child.to_html())
            
        return (
            f"<{self.tag}{self.props_to_html()}>{"".join(children_nodes)}</{self.tag}>"
        )