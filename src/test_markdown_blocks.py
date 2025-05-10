import unittest
from processes import markdown_to_blocks
from blocks import *


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_aggressive_whites(self):
        md = """
        



                This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line            





            - with items                                   




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- with items",
            ],
        )

    def test_is_header_block(self):
        nonce_str = "hey you"
        nonce_str_multiline = "   boogedie\ndooooo"
        good_nonced_headers = []

        for i in range(1,7):
            good_nonced_headers.append('#'*i + ' ' + nonce_str)
        for header_block in good_nonced_headers:
            self.assertEqual(is_header_block(header_block), True)

        good_nonced_headers_multiline = []

        for i in range(1,7):
            good_nonced_headers_multiline.append('#'*i + ' ' + nonce_str_multiline)
        for header_block in good_nonced_headers_multiline:
            self.assertEqual(is_header_block(header_block), True)

        bad_nonced_headers = []
        for i in range(1,7):
            bad_nonced_headers.append(' #'*i + ' ' + nonce_str)
        for header_block in bad_nonced_headers:
            self.assertEqual(is_header_block(header_block), False)

        self.assertEqual(is_header_block('#'*7 + ' ' + nonce_str_multiline), False)


if __name__ == "__main__":
    unittest.main()
