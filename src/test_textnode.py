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

from textnode import split_nodes_delimiter , extract_markdown_links, extract_markdown_images , split_nodes_image , split_nodes_link

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
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )






class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a *code block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_bold)
        expected_nodes = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_bold),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is a text with an image ![image](https://www.boot.dev)"
        images = extract_markdown_images(text)
        expected_images = [("image", "https://www.boot.dev")]
        self.assertEqual(images, expected_images)

    def test_extract_markdown_images_no_images(self):
        text = "This is a text with an image"
        images = extract_markdown_images(text)
        expected_images = []
        self.assertEqual(images, expected_images)

    def test_extract_markdown_images_multiple_images(self):
        text = "This is a text with an image ![image](https://www.boot.dev) and another ![image2](https://www.boot.dev/2)"
        images = extract_markdown_images(text)
        expected_images = [("image", "https://www.boot.dev"), ("image2", "https://www.boot.dev/2")]
        self.assertEqual(images, expected_images)

    def test_extract_markdown_links(self):
        text = "This is a text with a link [link](https://www.boot.dev)"
        links = extract_markdown_links(text)
        expected_links = [("link", "https://www.boot.dev")]
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_no_links(self):
        text = "This is a text with a link"
        links = extract_markdown_links(text)
        expected_links = []
        self.assertEqual(links, expected_links)

    def test_extract_markdown_links_multiple_links(self):
        text = "This is a text with a link [link](https://www.boot.dev) and another [link2](https://www.boot.dev/2)"
        links = extract_markdown_links(text)
        expected_links = [("link", "https://www.boot.dev"), ("link2", "https://www.boot.dev/2")]
        self.assertEqual(links, expected_links)



class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode("This is text with an image ![image](https://www.boot.dev)", text_type_text)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("image", text_type_image, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_no_image(self):
        node = TextNode("This is text with an image", text_type_text)
        new_nodes = split_nodes_image([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_image_multiple_images(self):
        node = TextNode("This is text with an image ![image](https://www.boot.dev) and another ![image2](https://www.boot.dev/2)", text_type_text)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an image ", text_type_text),
            TextNode("image", text_type_image, "https://www.boot.dev"),
            TextNode(" and another ", text_type_text),
            TextNode("image2", text_type_image, "https://www.boot.dev/2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)



class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode("This is text with a link [link](https://www.boot.dev)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("link", text_type_link, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_no_link(self):
        node = TextNode("This is text with a link", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [node]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_link_multiple_links(self):
        node = TextNode("This is text with a link [link](https://www.boot.dev) and another [link2](https://www.boot.dev/2)", text_type_text)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("link", text_type_link, "https://www.boot.dev"),
            TextNode(" and another ", text_type_text),
            TextNode("link2", text_type_link, "https://www.boot.dev/2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)
if __name__ == "__main__":
    unittest.main()

