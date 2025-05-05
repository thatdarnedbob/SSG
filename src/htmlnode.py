class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        html_props = ""
        for key, value in self.props.items():
            html_props += f' {key}="{value}"'
        return html_props
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        else:
            html_repr = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                html_repr += child.to_html()
            html_repr += f"</{self.tag}>"
            return html_repr
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"