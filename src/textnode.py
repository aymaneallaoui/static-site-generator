import itertools
from htmlnode import LeafNode, ParentNode, HTMLNode

import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            for i, text in enumerate(split_text):
                new_type = text_type if i % 2 else text_type_text
                new_nodes.append(TextNode(text, new_type))
    return new_nodes


def extract_markdown_images(text):
    """ return a list of tuples with the image text and url"""
    # the regex pattern to match markdown images r"!\[(.*?)\]\((.*?)\)"

    pattern = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text):
    """ return a list of tuples with the link text and url"""
    # the regex pattern to match markdown links r"\[(.*?)\]\((.*?)\)"

    pattern = r"\[(.*?)\]\((.*?)\)"
    return re.findall(pattern, text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            original_text = node.text
            images = extract_markdown_images(original_text)
            if len(images) == 0:
                new_nodes.append(node)
            else:
                start = 0
                for image in images:
                    image_markdown = f"![{image[0]}]({image[1]})"
                    image_start = original_text.find(image_markdown)
                    image_end = image_start + len(image_markdown)

                    text_before = original_text[start:image_start]
                    if text_before:
                        new_nodes.append(TextNode(text_before, text_type_text))
                    new_nodes.append(
                        TextNode(image[0], text_type_image, image[1]))
                    start = image_end
                text_after = original_text[start:]
                if text_after:
                    new_nodes.append(TextNode(text_after, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            original_text = node.text
            links = extract_markdown_links(original_text)
            if len(links) == 0:
                new_nodes.append(node)
            else:
                start = 0
                for link in links:
                    link_markdown = f"[{link[0]}]({link[1]})"
                    link_start = original_text.find(link_markdown)
                    link_end = link_start + len(link_markdown)

                    text_before = original_text[start:link_start]
                    if text_before:
                        new_nodes.append(TextNode(text_before, text_type_text))
                    new_nodes.append(
                        TextNode(link[0], text_type_link, link[1]))
                    start = link_end
                text_after = original_text[start:]
                if text_after:
                    new_nodes.append(TextNode(text_after, text_type_text))
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
block_type_paragraph = "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        block_type = detect_block_type(block)
        html_block = block_to_html_node(block, block_type)
        html_blocks.append(html_block)
    return ParentNode("div", html_blocks)


def markdown_to_blocks(markdown):
    lines = markdown.split("\n")
    blocks = []
    current_block = []
    for line in lines:
        if line.strip() == "":
            if current_block:
                blocks.append(current_block)
                current_block = []
        else:
            current_block.append(line)
            # Adding this condition to handle multiple heading blocks
            if detect_block_type(current_block) == block_type_heading:
                blocks.append(current_block)
                current_block = []
    if current_block:
        blocks.append(current_block)
    return blocks


def detect_block_type(block):
    first_line = block[0]
    if first_line.startswith("#"):
        return block_type_heading
    elif first_line.startswith("```"):
        return block_type_code
    elif first_line.startswith(">"):
        return block_type_quote
    elif first_line.startswith("* "):
        return block_type_unordered_list
    elif re.match(r"^\d+\.", first_line):
        return block_type_ordered_list
    else:
        return block_type_paragraph


def block_to_html_node(block, block_type):
    if block_type == block_type_heading:
        stripped = block[0].lstrip()
        heading_level = len(
            list(next((group for group in itertools.groupby(stripped)), ('#', 0))[1]))
        heading_level = min(heading_level, 6)
        content = stripped.lstrip("#").strip()
        return ParentNode(f"h{heading_level}", [text_node_to_html_node(node) for node in text_to_textnodes(content)])

    elif block_type == block_type_code:
        # Collect code block lines, excluding the first and last lines (```)
        code_lines = block[1:-1]
        # Ensure final newline is preserved
        code_text = "\n".join(code_lines) + "\n"
        # Correctly initialize LeafNode
        return ParentNode("pre", [LeafNode("code", code_text)])
    elif block_type == block_type_quote:
        quote_content = " ".join([line.lstrip("> ").strip() for line in block])
        return ParentNode("blockquote", [text_node_to_html_node(node) for node in text_to_textnodes(quote_content)])
    elif block_type == block_type_unordered_list:
        list_items = [line.lstrip("* ").strip() for line in block]
        return ParentNode("ul", [ParentNode("li", [text_node_to_html_node(node) for node in text_to_textnodes(item)]) for item in list_items])
    elif block_type == block_type_ordered_list:
        list_items = [line.lstrip("0123456789. ").strip() for line in block]
        return ParentNode("ol", [ParentNode("li", [text_node_to_html_node(node) for node in text_to_textnodes(item)]) for item in list_items])
    elif block_type == block_type_paragraph:
        paragraph_text = " ".join(block)
        return ParentNode("p", [text_node_to_html_node(node) for node in text_to_textnodes(paragraph_text)])
    else:
        raise ValueError(f"Invalid block type: {block_type}")


def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")
