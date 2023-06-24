import re
import xml.etree.ElementTree as etree
from markdown import util
from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor

SUP_RE = r"(\^)([\S]+?)(\^)"
SUB_RE = r"(\~)([\S]+?)(\~)"

class BlockQuoteEscaped(BlockProcessor):

    RE = re.compile(r'(^|\n)[ ]{0,3}(>|&gt;)[ ]?(.*)')

    def test(self, parent, block):
        return bool(self.RE.search(block)) and not util.nearing_recursion_limit()

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[:m.start()]  # Lines before blockquote
            # Pass lines before blockquote in recursively for parsing first.
            self.parser.parseBlocks(parent, [before])
            # Remove ``> `` from beginning of each line.
            block = '\n'.join(
                [self.clean(line) for line in block[m.start():].split('\n')]
            )
        sibling = self.lastChild(parent)
        if sibling is not None and sibling.tag == "blockquote":
            # Previous block was a blockquote so set that as this blocks parent
            quote = sibling
        else:
            # This is a new blockquote. Create a new parent element.
            quote = etree.SubElement(parent, 'blockquote')
        # Recursively parse block with blockquote as parent.
        # change parser state so blockquotes embedded in lists use `p` tags
        self.parser.state.set('blockquote')
        self.parser.parseChunk(quote, block)
        self.parser.state.reset()

    def clean(self, line):
        """ Remove ``>`` from beginning of a line. """
        m = self.RE.match(line)
        if line.strip() == ">" or line.strip() == "&gt;":
            return ""
        elif m:
            return m.group(3)
        else:
            return line

class EscapedExtension(Extension):
        def extendMarkdown(self, md):
            md.parser.blockprocessors.register(BlockQuoteEscaped(md.parser), 'quote_escaped', 20)

def makeExtension(**kwargs):
    return EscapedExtension(**kwargs)

if __name__ == '__main__':
    import doctest
    doctest.testfile('README.md')
