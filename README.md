# markdown_escaped
A python markdown extension for add HTML escaped symbols support

Extends the [Python Markdown](https://python-markdown.github.io/).
Adds the possibility to use escaped HTML caracters for markdown syntax, such as `&gt;` instead of `>` for blockquote.

Install through pip:

```bash
pip install markdown_escaped
```

To enable the markdown_escaped package and use it in your markdown generation just add it like so:

```python
import markdown

result = markdown.markdown(textToRender, extensions=["markdown_escaped",])
```

## List of supported caracters

 - `>` who is `&gt;` for blockquote

If you want an other caracter, open an issue or make a PR.

## Test string

It is a test:
> Yes it works!
Really good.

The real test:

&gt; And now ?
All is good!

Yeah !

### Raw string
`'It is a test:\n> Yes it works!\nReally good.\n\nThe real test:\n\n&gt; And now ?\nAll is good!\n\nYeah !'`
### Expected result
`'<p>It is a test:</p>\n<blockquote>\n<p>Yes it works!\nReally good.</p>\n</blockquote>\n<p>The real test:</p>\n<blockquote>\n<p>And now ?\nAll is good!</p>\n</blockquote>\n<p>Yeah !</p>'`
