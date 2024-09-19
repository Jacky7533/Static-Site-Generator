import unittest
from generate_page import *

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_with_whitespace(self):
        self.assertEqual(extract_title("#   Hello World  "), "Hello World")

    def test_extract_title_no_h1_header(self):
        with self.assertRaises(ValueError):
            extract_title("No title here")
    
    def test_extract_title_multiple_headers(self):
        self.assertEqual(extract_title("# First Title\n## Subtitle\n# Second Title"), "First Title")

if __name__ == '__main__':
    unittest.main()