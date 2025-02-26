from textnode import TextType,TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            first_delim = text.find(delimiter)
            second_delim = text.find(delimiter, first_delim + 1)


            if first_delim == -1 or second_delim == -1:
                raise ValueError("No matching delimiter found")

            before_text = text[:first_delim]
            middle_text = text[first_delim + len(delimiter):second_delim]
            after_text = text[second_delim + len(delimiter):]

            if before_text:
               new_nodes.append(TextNode(before_text, TextType.TEXT))
            if middle_text:
               new_nodes.append(TextNode(middle_text, text_type))
            if after_text:
               new_nodes.append(TextNode(after_text, TextType.TEXT))

    return new_nodes
