import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    # def __init__():
    #   super.__init__()
    #   self.test_case_one  = HTMLNode("p", "balls out", None, {
    #        "href": "https://www.google.com",
    #        "target": "_blank",
    #    })

    def test_repr(self):
        test_case_one  = HTMLNode("p", "balls out", None, {
            "href": "https://www.google.com",
            "target": "_blank",
        })
        print(test_case_one)
        print(test_case_one.props_to_html())

if __name__ == "__main__":
    unittest.main()