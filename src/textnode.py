from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    NORMAL = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "link"
    IMAGES = "image"


class TextNode:
    def __init__(self,text,text_type,url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.url == other.url and self.text == other.text and self.text_type == other.text_type

    def __repr__ (self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
        match text_node.text_type:
            case TextType.NORMAL:
                 return LeafNode(tag=None, value=text_node.text)

            case TextType.BOLD:
                return LeafNode(tag="b", value=text_node.text, props={})

            case TextType.ITALIC:
                return LeafNode(tag="i", value=text_node.text)

            case TextType.CODE:
                return LeafNode(tag="code", value=text_node.text)

            case TextType.LINKS:
                return LeafNode(
                       tag="a",
                       value=text_node.text,
                       props={"href": text_node.url}
                       )

            case TextType.IMAGES:
                return LeafNode(
                       tag="img",
                       value="",
                       props={"src": text_node.src, "alt": text_node.alt}
                       )   

            case _:
                raise InvalidTextNodeTypeError("Unsupported TextNode type.")



class InvalidTextNodeTypeError(Exception):
    def __init__(self, message="Invalid TextNode type supplied"):
        super().__init__(message)

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    
