class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        props_list = []
        for key, value in self.props.items():
            props_list.append(f' {key}="{value}"')
        return "".join(props_list)

    def __repr__(self):
      return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if props is None:  
            props = {}
        super().__init__(tag=tag, value=value, children=None, props=props)
   

    def to_html(self):
        if self.value is None:
          raise ValueError("Leaf node must have a value")
    
        if self.tag is None:
            return self.value
        else:
            if self.props:
                props_str = self.props_to_html()
                return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}>{self.value}</{self.tag}>"
class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag, value=None, children=children,props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a tag")
        
        if self.children is None:
            raise ValueError("Parent node must have children")

        if self.props:
             props_str = self.props_to_html()
             opening_tag = f"<{self.tag} {props_str}>"
        else:
             opening_tag = f"<{self.tag}>"

        children_html = ""
        for child in self.children:
            children_html += child.tohtml()



        closing_tag = f"</{self.tag}>"
        return f"{opening_tag}{children_html}{closing_tag}"






