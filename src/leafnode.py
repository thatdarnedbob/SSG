from htmlnode import HTMLNode

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props):
        if not value:
            raise ValueError("All leaf nodes must have a value")
        super(tag, value, None, props)
        