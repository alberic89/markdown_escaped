import re
import xml.etree.ElementTree as etree
from markdown import util
from markdown.extensions import Extension
from markdown.blockprocessors import BlockQuoteProcessor

class BlockQuoteEscaped(BlockQuoteProcessor):

    RE = re.compile(r'(^|\n)[ ]{0,3}&gt;[ ]?(.*)')

    def clean(self, line):
        """ Remove ``&gt;`` from beginning of a line. """
        m = self.RE.match(line)
        if line.strip() == "&gt;":
            return ""
        elif m:
            return m.group(2)
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
