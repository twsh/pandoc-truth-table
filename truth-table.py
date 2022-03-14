#!/usr/bin/env python3

"""
Pandoc filter using panflute
Take code blocks with the class 'ttable' and return a truth table as a Pandoc table
Example input:

```{.ttable}
P and Q
```

Tested with panflute 1.12.5 and pandoc 2.9.2.1

TODO: Find the logical vocabulary, and count everything else as a letter, rather than just taking
upper case:
'not', '-', '~', 'or', 'nor', 'xor', '!=', 'and', 'nand', '=>', 'implies', '='

"""

import re
import panflute as pf
import ttg


def latexify(txt):
    """
    Take some text and replace the logical vocabulary that ttg understands with LaTeX equivalents
    """
    # Use LaTeX symbols as in Forallx (roughly)
    substitutions = {
        "not": "\\lnot",
        "-": "\\lnot",
        "~": "\\lnot",
        "or": "\\lor",
        "nor": "\\downarrow",
        "xor": "\\veebar",
        "!=": "\\veebar",
        "and": "\\land",
        "nand": "\\uparrow",
        "implies": "\\rightarrow",
        "=>": "\\rightarrow",
        "=": "\\leftrightarrow",
    }

    regex = re.compile("(%s)" % "|".join(map(re.escape, substitutions.keys())))

    return regex.sub(lambda mo: substitutions[mo.string[mo.start() : mo.end()]], txt)


def mathify(elem, doc):
    """
    Take a Plain object and return a Plain object with its contents in a Math object
    """
    if isinstance(elem, pf.Plain):
        # Turn the paragraph into text (why can't I get its content?)
        latex = latexify(pf.stringify(elem))
        return pf.Plain(pf.Math(latex, format="InlineMath"))
    return None


def ttables(elem, doc):
    """
    Turn fenced code blocks into table objects if they have the .ttable class
    """
    # Run only for code blocks with the .ttable class
    if isinstance(elem, pf.CodeBlock) and "ttable" in elem.classes:
        # The formulae, as a list
        formulae = elem.text.split(",")
        # I need to get the letters in the formulaa, for the generator
        # This gets everything upper case, and puts them in order
        letters = sorted(set(re.findall("[A-Z]", elem.text)))
        # make the table with the truth-table-generator library
        truth_table = ttg.Truths(
            letters,
            formulae,
            # ints=False # use words, not numbers
        )
        # make the markdown table
        markdown_table = truth_table.as_tabulate(
            index=False,  # no line numbers
            table_format="simple",  # this is a format that Pandoc can read
        )
        # Replace '1' and '0' with 'T' and 'F'
        markdown_table = re.sub("1|True", "T", markdown_table)
        markdown_table = re.sub("0|False", "F", markdown_table)
        pandoc_table = pf.convert_text(markdown_table)[0]  # convert_text returns a list
        # The header should contain Math objects
        pandoc_table.header = pandoc_table.header.walk(mathify)
        pandoc_table.caption = [pf.Math(latexify(elem.text), format="InlineMath")]
        return pandoc_table
    return None


def main(doc=None):
    return pf.run_filter(ttables, doc=doc)


if __name__ == "__main__":
    main()
