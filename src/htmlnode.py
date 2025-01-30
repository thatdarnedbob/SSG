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