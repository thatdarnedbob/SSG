import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_both_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq_one_default(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_eq_neither_default(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://gmail.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://gmail.com")
        self.assertEqual(node, node2)

    def test_eq_url_diff(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://gmail.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://gmail.con")
        self.assertNotEqual(node, node2)

    def test_eq_text_type_diff(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://gmail.com")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://gmail.con")
        self.assertNotEqual(node, node2)

    def test_eq_text_diff(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://gmail.com")
        node2 = TextNode("This is a test node", TextType.BOLD, "https://gmail.con")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()