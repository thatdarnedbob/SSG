from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if is_header_block(block):
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH

def is_header_block(block):
    pattern = re.compile("#{1,6} .*", flags=re.DOTALL)
    return pattern.match(block) is not None

def is_code_block(block):
    pattern = re.compile("```.*```", flags=re.DOTALL)
    return pattern.match(block) is not None

def is_quote_block(block):
    pattern = re.compile(">.*")
    individual_lines = block.splitlines()
    default_val = True
    if len(individual_lines) == 0:
        return False
    for line in individual_lines:
        default_val = default_val and pattern.match(line) is not None
    return default_val

def is_unordered_list_block(block):
    pattern = re.compile("- .*")
    individual_lines = block.splitlines()
    default_val = True
    if len(individual_lines) == 0:
        return False
    for line in individual_lines:
        default_val = default_val and pattern.match(line) is not None
    return default_val

def is_ordered_list_block(block):
    individual_lines = block.splitlines()
    lines_number = len(individual_lines)
    default_val = True
    if len(individual_lines) == 0:
        return False
    
    for i in range(lines_number):
        pattern = re.compile(f"{i+1}\. .*")
        default_val = default_val and pattern.match(individual_lines[i]) is not None

    return default_val