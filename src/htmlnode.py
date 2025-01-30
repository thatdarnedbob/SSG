class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html_props = ""
        for key, value in self.props.items():
            html_props += " " + key +  ": " + value
        return html_props
    
    def __repr__(self):
        return f'''HTMLNode object
            tag: {self.tag}
            value: {self.value}
            children: {self.children}
            props: {self.props}'''

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props):
        if not value:
            raise ValueError("All leaf nodes must have a value")
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        else:
            return "<" + self.tag + self.props_to_html() + ">" + self.value + "</" + self.tag + ">"