import unittest
from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertListEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
            blocks,
        )

    def test_block_to_block_type_head(self):
        md = "# heading n°1"
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_quote(self):
        md = """
> quote num°1
> quote num°2
> quote num°3
"""
        stripped_md = md.strip()
        block_type = block_to_block_type(stripped_md)

        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_orderedlist(self):
        md = """
1. item num°1
2. item num°2
3. item num°3
"""
        stripped_md = md.strip()
        block_type = block_to_block_type(stripped_md)

        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        md = "just a normal pargraph over here"
        block_type = block_to_block_type(md)

        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblocks(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quotes(self):
        md = """

> here's quote n°1
> here's quote n°2
> here's quote n°3

"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><blockquote>here's quote n°1</blockquote><blockquote>here's quote n°2</blockquote><blockquote>here's quote n°3</blockquote></div>"
        )
    
    def test_headings(self):
        md = """
# main heading


### secondary heading
"""
        node = markdown_to_html_node(md)
        html = node.to_html()

        self.assertEqual(
            html,
            "<div><h1>main heading</h1><h3>secondary heading</h3></div>"
        )

    def test_extract_title_1header(self):
        md = """
some plain paragraph

# The main header here

### Sub header

"""
        header_text = extract_title(md)

        self.assertEqual(
            header_text,
            "The main header here"
        )

    def test_extract_title_no_header(self):
        md = """
no main header over

## just a sub-header
"""
        self.assertRaises(Exception, extract_title, md)

if __name__ == "__main__":
    unittest.main()
