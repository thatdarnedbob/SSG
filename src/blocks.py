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
    pass

def is_header_block(block):
    pattern = re.compile("#{1,6} .*", flags=re.DOTALL)
    return pattern.match(block) is not None

def is_code_block(block):
    pass

def is_quote_block(block):
    pass

def is_unordered_list_block(block):
    pass

def is_ordered_list_block(block):
    pass