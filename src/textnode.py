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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:  # Note: TEXT not NORMAL
            new_nodes.append(node)
            continue  # Skip to next iteration
        
        text = node.text
        first_delim = text.find(delimiter)
        if first_delim == -1:  # No delimiter found
            new_nodes.append(node)
            continue  # Skip to next iteration
            
        second_delim = text.find(delimiter, first_delim + len(delimiter))
        if second_delim == -1:  # No closing delimiter
            new_nodes.append(node)
            continue  # Skip to next iteration
            
        # We found both delimiters, now split the text
        before_text = text[:first_delim]
        middle_text = text[first_delim + len(delimiter):second_delim]
        after_text = text[second_delim + len(delimiter):]
        
        if before_text:
            new_nodes.append(TextNode(before_text, TextType.NORMAL))
        if middle_text:
            new_nodes.append(TextNode(middle_text, text_type))
        if after_text:
            new_nodes.append(TextNode(after_text, TextType.NORMAL))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL: 
            new_nodes.append(old_node)
            continue
            
        images = extract_markdown_images(old_node.text)
        
        if not images:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        
        for image_alt, image_url in images:
            image_markdown = f"![{image_alt}]({image_url})"
            sections = remaining_text.split(image_markdown, 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_url))
            
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL: 
            new_nodes.append(old_node)
            continue
            
        links = extract_markdown_links(old_node.text)
        
        if not links:
            new_nodes.append(old_node)
            continue
            
        remaining_text = old_node.text
        
        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            sections = remaining_text.split(link_markdown, 1)
            
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            
            new_nodes.append(TextNode(link_text, TextType.LINKS, link_url))
            
            if len(sections) > 1:
                remaining_text = sections[1]
            else:
                remaining_text = ""
        
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.NORMAL))
    
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]  # Start with a single node
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Now split by delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    stripped_blocks = [block.strip() for block in blocks]
    
    non_empty_blocks = [block for block in stripped_blocks if block]
    
    return non_empty_blocks

