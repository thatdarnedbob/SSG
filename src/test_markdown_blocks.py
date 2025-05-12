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

    def test_is_code_block(self):
        nonce_str = "hey you"
        nonce_str_multiline = "   boogedie\ndooooo"
        good_nonced_headers = []
        good_nonced_headers_multiline = []
        bad_nonced_headers = []

        good_nonced_headers.append('```' + nonce_str + '```')
        good_nonced_headers_multiline.append('```' + nonce_str_multiline + '```')

        bad_nonced_headers.append('```' + nonce_str + '``')

        self.assertEqual(is_code_block(good_nonced_headers[-1]), True)
        self.assertEqual(is_code_block(good_nonced_headers_multiline[-1]), True)
        self.assertEqual(is_code_block(bad_nonced_headers[-1]), False)

    def test_is_quote_block(self):
        nonce_strs_1 = ["hey you\n",
                        "you might be thinking\n",
                        "this is just a unit test\n",
                        "but it ain't\n"]
        nonce_strs_2 = ["not a single\n",
                        "line of code\n",
                        "can eat a cherry\n"]
        good_nonced_block = ''
        bad_nonced_block = ''

        for nonce in nonce_strs_1:
            good_nonced_block = good_nonced_block + ">" + nonce
        for nonce in nonce_strs_2:
            bad_nonced_block = bad_nonced_block + ">" + nonce
        bad_nonced_block += " >... unless?"

        self.assertEqual(is_quote_block(good_nonced_block), True)
        self.assertEqual(is_quote_block(bad_nonced_block), False)
        
        good_nonced_block += "never again, ya know?"
        self.assertEqual(is_quote_block(good_nonced_block), False)

    def test_is_unordered_list_block(self):
        nonce_strs_1 = ["hey you\n",
                        "you might be thinking\n",
                        "this is just a unit test\n",
                        "but it ain't\n"]
        nonce_strs_2 = ["not a single\n",
                        "line of code\n",
                        "can eat a cherry\n"]
        good_nonced_block = ''
        bad_nonced_block = ''

        for nonce in nonce_strs_1:
            good_nonced_block = good_nonced_block + "- " + nonce
        for nonce in nonce_strs_2:
            bad_nonced_block = bad_nonced_block + "- " + nonce
        bad_nonced_block += "-... unless?"

        self.assertEqual(is_unordered_list_block(good_nonced_block), True)
        self.assertEqual(is_unordered_list_block(bad_nonced_block), False)
        
        good_nonced_block += "-never again, ya know?"
        self.assertEqual(is_unordered_list_block(good_nonced_block), False)

    def test_is_ordered_list_block(self):
        nonce_strs_1 = ["hey you\n",
                        "you might be thinking\n",
                        "this is just a unit test\n",
                        "but it ain't\n"]
        nonce_strs_2 = ["not a single\n",
                        "line of code\n",
                        "can eat a cherry\n"]
        good_nonced_block = ''
        bad_nonced_block = ''

        for i in range(len(nonce_strs_1)):
            good_nonced_block = good_nonced_block + f"{i+1}. " + nonce_strs_1[i]
        for i in range(len(nonce_strs_2)):
            bad_nonced_block = bad_nonced_block + f"{i} " + nonce_strs_2[i]

        self.assertEqual(is_ordered_list_block(good_nonced_block), True)
        self.assertEqual(is_ordered_list_block(bad_nonced_block), False)
        
        good_nonced_block += "7. never again, ya know?"
        self.assertEqual(is_ordered_list_block(good_nonced_block), False)


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
