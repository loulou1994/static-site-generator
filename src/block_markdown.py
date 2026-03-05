from enum import Enum
from textnode import TextNode, text_node_to_html_node, NODE_TYPE
from htmlnode import ParentNode
from inline_markdown import text_to_textnode

import os

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE= "code"
    QUOTE= "quote"
    ORDERED_LIST= "ordered_list"
    UNORDERED_LIST= "unordered_list"

def markdown_to_blocks(markdown):
    markdown_blocks = markdown.split("\n\n")
    parsed_markdown_blocks = []

    for markdown_block in markdown_blocks:
        if markdown_block == "":
            continue
        parsed_markdown_blocks.append(markdown_block.strip())

    return parsed_markdown_blocks

def block_to_block_type(markdown):
    lines = markdown.split("\n")

    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    
    if markdown.startswith("#"):
        count = 0
        for chr in markdown:
            if chr == "#":
                count += 1
            else:
                break
        
        if 1 <= count <= 6 and markdown[count] == " ":
            return BlockType.HEADING
            

    if all(line.startswith("> ") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    is_ordered = True
    count = 0
    for item in lines:
        if item == "":
            continue

        count += 1
        prefix = f"{count}. "
        if not item.startswith(prefix):
            is_ordered = False
            break
    
    if is_ordered:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks_list = markdown_to_blocks(markdown)
    block_nodes_list = []

    for block in blocks_list:
        # print(block)
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block, block_type)

        if block_type == BlockType.QUOTE:
            block_nodes_list.extend(block_node)
        else:
            block_nodes_list.append(block_node)
    
    return ParentNode("div", block_nodes_list)

def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    
    raise ValueError("Invalid block type")

def code_to_html_node(block):
    # Strip the ``` from start and end
    parsed_block = block.strip("```")[1:]
    # print(parsed_block)
    leaf_node_code = text_node_to_html_node(TextNode(parsed_block, NODE_TYPE.CODE))

    return ParentNode("pre", [leaf_node_code])

def paragraph_to_html_node(block):
    stripped_block = block.split("\n")
    parsed_block = " ".join(stripped_block)
    leaf_nodes_list = text_to_children(parsed_block)

    return ParentNode("p", leaf_nodes_list)

def heading_to_html_node(block):
    head_lvl = 0
    for chr in block:
        if chr == "#":
            head_lvl += 1
        else:
            break

    leaf_nodes_list = text_to_children(block[head_lvl+1:])

    return ParentNode(f"h{head_lvl}", leaf_nodes_list)

def quote_to_html_node(block):
    lines = block.strip().split("\n")
    parent_nodes_list = []

    for line in lines:
        leaf_nodes_list = text_to_children(line[2:])

        parent_nodes_list.append(ParentNode("blockquote", leaf_nodes_list))
    
    return parent_nodes_list

def ulist_to_html_node(block):
    lines = block.strip().split("\n")
    nested_parents_list = []

    for line in lines:
        leaf_nodes_list = text_to_children(line[2:])
        
        nested_parents_list.append(ParentNode("li", leaf_nodes_list))
    
    return ParentNode("ul", nested_parents_list)

def olist_to_html_node(block):
    lines = block.strip().split("\n")
    nested_parents_list = []

    for line in lines:
        leaf_nodes_list = text_to_children(line[3:])
        
        nested_parents_list.append(ParentNode("li", leaf_nodes_list))
    
    return ParentNode("ol", nested_parents_list)

def text_to_children(text):
    text_nodes_list = text_to_textnode(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes_list]

def extract_title(markdown):
    md_blocks = markdown_to_blocks(markdown)

    for block in md_blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            head_lvl = 0

            for chr in block:
                if chr == "#":
                    head_lvl += 1
                else:
                    break

            if head_lvl == 1:
                return block[head_lvl+1:]
    
    raise Exception("Couldn't find a valid h1 header")