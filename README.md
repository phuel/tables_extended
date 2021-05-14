# Tables-Extended

## Summary

This is an extended version of the [tables](https://python-markdown.github.io/extensions/tables/) extension of [Python-Markdown](https://python-markdown.github.io/). It contains addtions from the [cell_row_span](https://github.com/Neepawa/cell_row_span) extension and allows to create tables without header.

`tables_extended` is backward compatible to `tables` and nearly backward compatible to `cell_row_span`.

## Syntax

The `tables_extended` extension can be used to create tables using markdown:

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

Like with the `cell_row_span` extension empty cells are replaced horizontally using the `colspan` attribute on the next non-empty cell to the left.

Empty cells below a cell until a cell containing an underscore as the first and the last character are replaced with a `rowspan` attribute on the non-empty cell. By default the text in a cell with a rowspan is vertically aligned with e default alignment `baseline`. Other vertical alignments can be selected by adding a special character after the first underscore in the terminating line.

* `^` sets an alignmen to the top
* `-` sets middle alignment (new with `tables_extended`)
* `=` sets bottom aligment

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
