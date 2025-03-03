from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    # Check if it's a heading (starts with 1-6 # followed by a space)
    if block.startswith(('#', '##', '###', '####', '#####', '######')):
        # Make sure it's followed by a space
        parts = block.split(' ', 1)
        if len(parts) > 1 and all(c == '#' for c in parts[0]) and len(parts[0]) <= 6:
            return BlockType.HEADING
    
    # Check if it's a code block (starts and ends with ```)
    if block.startswith('```') and block.endswith('```'):
        return BlockType.CODE
    
    # Check if it's a quote (every line starts with >)
    lines = block.split('\n')
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    # Check if it's an unordered list (every line starts with - followed by space)
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    
    # Check if it's an ordered list
    if all(len(line.split('. ', 1)) > 1 and line.split('. ', 1)[0].isdigit() for line in lines):
        # Check if numbers start at 1 and increment by 1
        numbers = [int(line.split('. ', 1)[0]) for line in lines]
        if numbers[0] == 1 and all(numbers[i] == numbers[i-1] + 1 for i in range(1, len(numbers))):
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH



