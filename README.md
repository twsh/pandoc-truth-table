# pandoc-truth-table

A [Pandoc](https://pandoc.org/) [filter](https://pandoc.org/filters.html) to generate [truth tables](https://en.wikipedia.org/wiki/Truth_table) from [propositional calculus](https://en.wikipedia.org/wiki/Propositional_calculus) formulae.

Usage:

`$ pandoc --filter truth-table.py foo.md`


    ```{.ttable}
    P and Q, P
    ```

Uses [panflute](https://pypi.org/project/panflute/) and [truth-table-generator](https://pypi.org/project/truth-table-generator/).
