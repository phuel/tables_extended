# Tables-Extended

## Summary

This is an extended version of the [tables](https://python-markdown.github.io/extensions/tables/) extension of [Python-Markdown](https://python-markdown.github.io/). It contains addtions from the [cell_row_span](https://github.com/Neepawa/cell_row_span) extension and allows to create tables without header.

`tables_extended` is backward compatible to `tables` and nearly backward compatible to `cell_row_span`.

## Syntax

### Basic  table creation

The `tables_extended` extension can be used to create tables using markdown like the default [tables](https://python-markdown.github.io/extensions/tables/) extension:

```text
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```

renders as

```text
.-------------------------------.
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
`-------------------------------`
```

The separator row can be used to specify the horizontal alignment of the cells' content:

```text
Header 1 | Header 2 | Header 3
:------- | :------: | -------:
Cell 1   | Cell 2   | Cell 3
```

renders as

```text
.-------------------------------------------.
| Header 1    |   Header 2   |     Header 3 |
| ----------- | ------------ | ------------ |
| Cell 1      |    Cell 2    |       Cell 3 |
`-------------------------------------------`
```

### Tables without header

If no row is provided above the separator line, no header is generated:

```text
------ | ------
Cell 1 | Cell 2
Cell 3 | Cell 4
```

becomes

```text
.-----------------.
| Cell 1 | Cell 2 |
| Cell 3 | Cell 4 |
`-----------------`
```

### Merging of columns or rows

```text
| Column 1                | Col 2 | Big row span   |
|:-----------------------:|-------| -------------- |
| r1_c1 spans two cols           || One large cell |
| r2_c1 spans two rows    | r2_c2 |                |
|_^                      _| r3_c2 |                |
|    ______ &#20;         | r4_c2 |_              _|
```

The example renders as:

```text
.--------------------------------------------------.
|        Column 1         | Col 2 |  Big row span  |
|---------------------------------+----------------|
|      r1_c1 spans two cols       |                |
|---------------------------------|                |
|  r2_c1 spans two rows   | r2_c2 |                |
|                         |-------| One large cell |
|                         | r3_c2 |                |
|-------------------------+-------|                |
|          ____           | r4_c2 |                |
`--------------------------------------------------'
```

To span cells across multiple columns, end them with two or more consecutive
vertical bars. Cells to the left will be merged together, as many cells are
there are bars. In the example above, there are two bars at the end of cell
2 on row 1, so the two cells to the left of it (numbers 1 and 2) are merged.

To span cells across rows, fill the cell on the last row with at least two
underscores, one at the start and the other at the end of its content, and no
other characters than spaces, underscores, `^`, `-` or `=`. This is referred to as
the *marker.* The cell with the marker and all the empty cells above it to the
first non-empty cell will be made into a single cell, with the content of the
non-empty cell. See column 3 ("Big row span") in the example.

By default the contents are vertically aligned using `baseline` alignment, which
is the default used by browsers. To
align to the top, include at least one `^` character in the marker between the
two underscores; for example, `|_^^^_|` or simply `|_^   _|`. See row 2 in
column 1 of the example, which is merged with row 3 and aligned at the top. To
align to the bottom, use at least one `=` character between the underscores;
for example, `|_ = _|`. To align in the middle of the cell, include at least
one `-` character in the marker row. Including more than one of `^`, `-` and `=`
in a marker raises a `ValueError` exception.

Vertical alignment codes:
* `^` sets an alignmen to the top
* `-` sets middle alignment (new with `tables_extended`)
* `=` sets bottom aligment

Note: If this extension finds a cell with at least two underscores and no other
characters other than spaces, `^` or `=`, it assumes it's a row span marker and
attempts to process it. If you need a cell that looks like a marker (generally
one with only underscores in it), add the text `&#20;` as well---this extension
won't process it as a row span marker and Markdown will change the `&#20;` to a
space.


## Installation

Either clone this repository or download the released package from github and unpack it.

Change into the new directory. `tables_extended` can now be installed using `install.sh`,
which installs the package using `pip`:
```bash
pip install .
```
or use the `setup.py` script:
```bash
python setup.py install --user
```


## Usage

See [Extensions](https://python-markdown.github.io/extensions/) for general extension usage. Use `tables_extended`
as the name of the extension.

This extension does not accept any special configuration options.

The extension can be used by either providing the markdown processor with an extension instance
```python
from tables_extended import TableExtension

markdown.markdown(some_text, extensions=[TableExtension()])
```
or by using the extension name
```python
markdown.markdown(some_text, extensions=['tables_extended'])
```
