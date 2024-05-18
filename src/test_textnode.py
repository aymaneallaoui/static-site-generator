import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from textnode import split_nodes_delimiter, extract_markdown_links, extract_markdown_images, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, markdown_to_html_node

from htmlnode import ParentNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_text)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_text,
                        "https://www.lol.com")
        node2 = TextNode("This is a text node",
                         text_type_text, "https://www.lol.com")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text,
                        "https://www.lol.com")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.lol.com)", repr(node)
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode(
            "This is text with a *code block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_bold)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is a text with an image ![image](https://www.lol.com)"
        images = extract_markdown_images(text)
        expected_images = [("image", "https://www.lol.com")]
        self.assertEqual(images, expected_images)

    def test_extract_markdown_images_no_images(self):
        text = "This is a text with an image"
        images = extract_markdown_images(text)
        expected_images = []
        self.assertEqual(images, expected_images)

    def test_extract_markdown_images_multiple_images(self):
        text = "This is a text with an image ![image](https://www.lol.com) and another ![image2](https://www.lol.com/2)"
        images = extract_markdown_images(text)
        expected_images = [("image", "https://www.lol.com"),
                           ("image2", "https://www.lol.com/2")]
        self.assertEqual(images, expected_images)

    def test_extract_markdown_links(self):
        text = "This is a text with a link [link](https://www.lol.com)"
        links = extract_markdown_links(text)
        expected_links = [("link", "https://www.lol.com")]
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_no_links(self):
        text = "This is a text with a link"
        links = extract_markdown_links(text)
        expected_links = []
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_multiple_links(self):
        text = "This is a text with a link [link](https://www.lol.com) and another [link2](https://www.lol.com/2)"
        links = extract_markdown_links(text)
        expected_links = [("link", "https://www.lol.com"),
                          ("link2", "https://www.lol.com/2")]
        self.assertEqual(links, expected_links)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![image](https://www.lol.com)", text_type_text)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("image", text_type_image, "https://www.lol.com"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_no_image(self):
        node = TextNode("This is text with an image", text_type_text)
        new_nodes = split_nodes_image([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_multiple_images(self):
        node = TextNode(
            "This is text with an image ![image](https://www.lol.com) and another ![image2](https://www.lol.com/2)", text_type_text)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("image", text_type_image, "https://www.lol.com"),
            TextNode(" and another ", text_type_text),
            TextNode("image2", text_type_image, "https://www.lol.com/2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [link](https://www.lol.com)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("link", text_type_link, "https://www.lol.com"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_no_link(self):
        node = TextNode("This is text with a link", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            "This is text with a link [link](https://www.lol.com) and another [link2](https://www.lol.com/2)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("link", text_type_link, "https://www.lol.com"),
            TextNode(" and another ", text_type_text),
            TextNode("link2", text_type_link, "https://www.lol.com/2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text ** with an * italic * word and a `code block` and an ![image](https: // storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a[link](https: // lol.com)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", text_type_text),
            TextNode("text ", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode(" italic ", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image,
                     "https: // storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a", text_type_text),
            TextNode("link", text_type_link, "https: // lol.com"),
        ]
        self.assertEqual(nodes, expected_nodes)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = "This is a text\n\nThis is another text"
        blocks = markdown_to_blocks(markdown)
        expected_blocks = [
            ["This is a text"],
            ["This is another text"],
        ]
        self.assertEqual(blocks, expected_blocks)


def compare_nodes(node1, node2):
    if type(node1) != type(node2):
        return False, f"Type mismatch: {type(node1)} != {type(node2)}"
    if node1.tag != node2.tag:
        return False, f"Tag mismatch: {node1.tag} != {node2.tag}"
    if node1.value != node2.value:
        return False, f"Value mismatch: {node1.value} != {node2.value}"
    if node1.props != node2.props:
        return False, f"Props mismatch: {node1.props} != {node2.props}"
    if isinstance(node1, ParentNode):
        if len(node1.children) != len(node2.children):
            return False, f"Children count mismatch: {len(node1.children)} != {len(node2.children)}"
        for child1, child2 in zip(node1.children, node2.children):
            are_equal, message = compare_nodes(child1, child2)
            if not are_equal:
                return False, message
    return True, "Nodes are equal"


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_empty_string(self):
        markdown = ""
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [])
        self.assertEqual(node, expected_node)

    def test_single_paragraph(self):
        markdown = "This is a single paragraph."
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode("p", [LeafNode(None, "This is a single paragraph.")]),
        ])
        self.assertEqual(node, expected_node)

    def test_multiple_paragraphs(self):
        markdown = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode("p", [LeafNode(None, "First paragraph.")]),
            ParentNode("p", [LeafNode(None, "Second paragraph.")]),
            ParentNode("p", [LeafNode(None, "Third paragraph.")]),
        ])
        self.assertEqual(node, expected_node)

    def test_headings(self):
        markdown = "# Heading 1\n## Heading 2\n### Heading 3"
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode("h1", [LeafNode(None, "Heading 1")]),
            ParentNode("h2", [LeafNode(None, "Heading 2")]),
            ParentNode("h3", [LeafNode(None, "Heading 3")]),
        ])

        self.assertEqual(node, expected_node)

    def test_inline_formatting(self):
        markdown = "This is **bold**, *italic*, `code`, [link](http://example.com), and ![image](http://example.com/image.png)"
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "This is "),
                LeafNode("b", "bold"),
                LeafNode(None, ", "),
                LeafNode("i", "italic"),
                LeafNode(None, ", "),
                LeafNode("code", "code"),
                LeafNode(None, ", "),
                LeafNode("a", "link", {"href": "http://example.com"}),
                LeafNode(None, ", and "),
                LeafNode(
                    "img", "", {"src": "http://example.com/image.png", "alt": "image"})
            ]),
        ])
        self.assertEqual(node, expected_node)

    def test_block_quotes(self):
        markdown = "> This is a block quote.\n> It spans multiple lines."
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode("blockquote", [
                LeafNode(None, "This is a block quote. It spans multiple lines.")
            ]),
        ])
        self.assertEqual(node, expected_node)

    def test_unordered_list(self):
        markdown = "* Item 1\n* Item 2\n* Item 3"
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [LeafNode(None, "Item 1")]),
                ParentNode("li", [LeafNode(None, "Item 2")]),
                ParentNode("li", [LeafNode(None, "Item 3")]),
            ]),
        ])
        self.assertEqual(node, expected_node)

    def test_ordered_list(self):
        markdown = "1. First item\n2. Second item\n3. Third item"
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode("ol", [
                ParentNode("li", [LeafNode(None, "First item")]),
                ParentNode("li", [LeafNode(None, "Second item")]),
                ParentNode("li", [LeafNode(None, "Third item")]),
            ]),
        ])
        self.assertEqual(node, expected_node)

    def test_code_block(self):
        markdown = "```\ndef hello():\n    print('Hello, world!')\n```"
        node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", [
            ParentNode(
                "pre", [LeafNode("code", "def hello():\n    print('Hello, world!')\n")])
        ])

        self.assertEqual(node, expected_node)


class TestMarkdownToHTMLClassNames(unittest.TestCase):

    def test_heading_with_class(self):
        markdown = "# Heading {$class=card}"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)

        heading = html_node.children[0]
        self.assertIsInstance(heading, ParentNode)
        self.assertEqual(heading.tag, "h1")
        self.assertEqual(heading.props, {"class": "card"})
        self.assertEqual(heading.children[0].value, "Heading")

    def test_paragraph_with_class(self):
        markdown = "This is a paragraph. {$class=card}"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)

        paragraph = html_node.children[0]
        self.assertIsInstance(paragraph, ParentNode)
        self.assertEqual(paragraph.tag, "p")
        self.assertEqual(paragraph.props, {"class": "card"})
        self.assertEqual(paragraph.children[0].value, "This is a paragraph.")

    def test_code_block_with_class(self):
        markdown = "```\nCode block\n``` {$class=code-class}"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)

        code_block = html_node.children[0]
        self.assertIsInstance(code_block, ParentNode)
        self.assertEqual(code_block.tag, "pre")
        self.assertEqual(code_block.props, {"class": "code-class"})

        code = code_block.children[0]
        self.assertIsInstance(code, LeafNode)
        self.assertEqual(code.tag, "code")
        self.assertEqual(code.value, "Code block\n")

    def test_quote_with_class(self):
        markdown = "> This is a quote. {$class=quote-class}"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)

        blockquote = html_node.children[0]
        self.assertIsInstance(blockquote, ParentNode)
        self.assertEqual(blockquote.tag, "blockquote")
        self.assertEqual(blockquote.props, {"class": "quote-class"})
        self.assertEqual(blockquote.children[0].value, "This is a quote.")

    def test_list_with_class(self):
        markdown = "* Item 1\n* Item 2 {$class=list-class}"
        html_node = markdown_to_html_node(markdown)
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 1)

        ul = html_node.children[0]
        self.assertIsInstance(ul, ParentNode)
        self.assertEqual(ul.tag, "ul")
        self.assertEqual(ul.props, {"class": "list-class"})
        self.assertEqual(len(ul.children), 2)

        li1 = ul.children[0]
        self.assertIsInstance(li1, ParentNode)
        self.assertEqual(li1.tag, "li")
        self.assertEqual(li1.children[0].value, "Item 1")

        li2 = ul.children[1]
        self.assertIsInstance(li2, ParentNode)
        self.assertEqual(li2.tag, "li")
        self.assertEqual(li2.children[0].value, "Item 2")


if __name__ == '__main__':
    unittest.main()
