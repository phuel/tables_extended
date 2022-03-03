"""
Extended Tables Extension for Python-Markdown
=============================================

Allows to create tables with colspans and rowspans and optional
header with Python-Markdown

Copyright 2021 phuel

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)

based on:

    Tables Extension for Python-Markdown
    ====================================

    Added parsing of tables to Python-Markdown.

    See <https://Python-Markdown.github.io/extensions/tables>
    for documentation.

    Original code Copyright 2009 [Waylan Limberg](http://achinghead.com)

    All changes Copyright 2008-2014 The Python Markdown Project

    License: [BSD](https://opensource.org/licenses/bsd-license.php)

And

    Table Cell and Row Span extension for Python Markdown
    =====================================================

    Adds spanning for rows and cells in tables.

    Author:  Neepawa


    License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""

from markdown import Extension
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re

PIPE_NONE = 0
PIPE_LEFT = 1
PIPE_RIGHT = 2

class Cell():
    def __init__(self, text, align):
        self.text = None
        if text != '':
            self.text = text.strip(' ')
        self.align = align
        self.colspan = 1
        self.rowspan = 1
        self.valign = None

class TableProcessor(BlockProcessor):
    """ Process Tables. """

    SEPARATOR_CHARS_SET = set('|:- ')

    RE_CODE_PIPES = re.compile(r'(?:(\\\\)|(\\`+)|(`+)|(\\\|)|(\|))')
    RE_END_BORDER = re.compile(r'(?<!\\)(?:\\\\)*\|$')

    RE_row_span_marker = re.compile(r'^_[_^=\- ]*_$')
    RE_valign_top = re.compile(r'.*\^')
    RE_valign_bottom = re.compile(r'.*=')
    RE_valign_middle = re.compile(r'.*-')

    def __init__(self, parser):
        self.border = False
        self.separator = ''
        super().__init__(parser)

    def test(self, parent, block):
        """
        Ensure first two rows (column header and separator row) are valid table rows.

        Keep border check and separator row do avoid repeating the work.
        """
        is_table = False
        rows = [row.strip(' ') for row in block.split('\n')]
        if len(rows) > 1:
            # The separator row can either be the first or the second row.
            # If the separator row is the first row, no table header is generated.
            self.separator_row = self._get_separator_row(rows)
            if self.separator_row < 0:
                return False

            self.separator = self._split_row(rows[self.separator_row])
            
            # Use the first row (separator or text) to determine the border.
            row0 = rows[0]
            self.border = PIPE_NONE
            if row0.startswith('|'):
                self.border |= PIPE_LEFT
            if self.RE_END_BORDER.search(row0) is not None:
                self.border |= PIPE_RIGHT
            
            # Use the first text row to determine the column count.
            if self.separator_row == 0:
                row0 = rows[1]
            row = self._split_row(row0)
            row0_len = len(row)
            is_table = row0_len > 1

            # Each row in a single column table needs at least one pipe.
            if not is_table and row0_len == 1 and self.border:
                for index in range(1, len(rows)):
                    is_table = rows[index].startswith('|')
                    if not is_table:
                        is_table = self.RE_END_BORDER.search(rows[index]) is not None
                    if not is_table:
                        break

            if is_table:
                row = self._split_row(rows[self.separator_row])
                is_table = (len(row) == row0_len) and set(''.join(row)) <= self.SEPARATOR_CHARS_SET
                if is_table:
                    self.separator = row

        return is_table

    def run(self, parent, blocks):
        """ Parse a table block and build table. """
        block = blocks.pop(0).split('\n')
        header = None
        rows = None
        if self.separator_row > 0:
            header = block[0]
            rows = block[2:]
        else:
            rows = block[1:]

        # Get alignment of columns
        align = []
        for c in self.separator:
            c = c.strip(' ')
            if c.startswith(':') and c.endswith(':'):
                align.append('center')
            elif c.startswith(':'):
                align.append('left')
            elif c.endswith(':'):
                align.append('right')
            else:
                align.append(None)

        # Build table
        table = etree.SubElement(parent, 'table')
        if header is not None:
            thead = etree.SubElement(table, 'thead')
            cells = self._parse_row(header, align)
            self._merge_spans([ cells ])
            self._build_row(cells, thead)
        tbody = etree.SubElement(table, 'tbody')
        if len(rows) == 0:
            # Handle empty table
            self._build_empty_row(tbody, align)
        else:
            cells = []
            for row in rows:
                row_cells = self._parse_row(row, align)
                cells.append(row_cells)
            self._merge_spans(cells)
            for row in cells:
                self._build_row(row, tbody)

    def _get_separator_row(self, rows):
        """Search for the separator row.
           Returns the row index (either 0, 1 or -1 (if no separator row has been found))."""
        if set(''.join(rows[0])) <= self.SEPARATOR_CHARS_SET:
            return 0
        if set(''.join(rows[1])) <= self.SEPARATOR_CHARS_SET:
            return 1
        return -1
       
    def _build_empty_row(self, parent, align):
        """Build an empty row."""
        tr = etree.SubElement(parent, 'tr')
        count = len(align)
        while count:
            etree.SubElement(tr, 'td')
            count -= 1

    def _build_row(self, cells, parent):
        """ Given a row of parsed cells, build table cells. """
        tr = etree.SubElement(parent, 'tr')
        tag = 'td'
        if parent.tag == 'thead':
            tag = 'th'
        for cell in cells:
            if cell is None:
                continue
            c = etree.SubElement(tr, tag)
            c.text = cell.text
            if cell.align is not None:
                c.set('align', cell.align)
            if cell.colspan > 1:
                c.set('colspan', str(cell.colspan))
            if cell.rowspan > 1:
                c.set('rowspan', str(cell.rowspan))
            if cell.valign is not None:
               c.set('valign', cell.valign)
            

    def _merge_spans(self, rows):
        """Transforms adjacent empty cells into colspans or rowspans."""
        for row_index in range(len(rows)):
            for col_index in range(len(rows[row_index])):
                self._merge_spans_for_cell(rows, row_index, col_index)

    def _merge_spans_for_cell(self, rows, row_index, col_index):
        """Starting from one cell transforms adjacent empty cells into colspans or rowspans."""
        nrows = len(rows)
        row = rows[row_index]
        ncols = len(row)
        cell = row[col_index]
        
        # If the cell is already collapsed nothing needs to be done anymore.
        if cell is None:
            return

        # Check for empty cells to collapse right of the current cell.
        right = col_index + 1
        while right < ncols:
            if row[right] is None:
                break
            if row[right].text is not None:
                break
            cell.colspan += 1
            right += 1

        # Check for empty cells to collapse below the current cell.
        rowspan_found = False
        down = row_index + 1
        while down < nrows:
            if rows[down][col_index] is None:
                break
            text = rows[down][col_index].text
            if text is not None:
                if self.RE_row_span_marker.match(text):
                    # The end marker was found, so include this cell
                    # in the rowspan and set the vertical alignment.
                    cell.rowspan += 1
                    if self.RE_valign_top.match(text):
                        cell.valign = 'top'
                    if self.RE_valign_bottom.match(text):
                        if cell.valign is not None:
                            raise ValueError('Can only use one of ^ (top), - (middle) or = (bottom) codes in one row span marker.')
                        cell.valign = 'bottom'
                    if self.RE_valign_middle.match(text):
                        if cell.valign is not None:
                            raise ValueError('Can only use one of ^ (top), - (middle) or = (bottom) codes in one row span marker.')
                        cell.valign = 'middle'
                    rowspan_found = True
                    break
                elif text.strip(' ') != '':
                    break
            cell.rowspan += 1
            down += 1
        if not rowspan_found:
            cell.rowspan = 1
        
        # Replace all collapsed cells with None.
        for r in range(0, cell.rowspan):
            for c in range(0, cell.colspan):
                if r == 0 and c == 0:
                    # Keep the current cell.
                    continue
                rows[row_index + r][col_index + c] = None

    def _parse_row(self, row, align):
        """Split a row and create cells for each row item."""
        texts = self._split_row(row)
        cells = [ None ] * len(align)
        # We use align here rather than cells to ensure every row
        # contains the same number of columns.
        for i, a in enumerate(align):
            try:
                cells[i] = Cell(texts[i], a)
            except IndexError:  # pragma: no cover
                cells[i] = Cell('', a)
        return cells

    def _split_row(self, row):
        """ split a row of text into list of cells. """
        row = row.strip(' ')
        if self.border:
            if row.startswith('|'):
                row = row[1:]
            row = self.RE_END_BORDER.sub('', row)
        else:
            # Add space characters in front and back to avoid mistaking empty
            # cells at the beginning or end as cells that have to be collapsed.
            row = ' ' + row + ' '
        return self._split(row)

    def _split(self, row):
        """ split a row of text with some code into a list of cells. """
        elements = []
        pipes = []
        tics = []
        tic_points = []
        tic_region = []
        good_pipes = []

        # Parse row
        # Throw out \\, and \|
        for m in self.RE_CODE_PIPES.finditer(row):
            # Store ` data (len, start_pos, end_pos)
            if m.group(2):
                # \`+
                # Store length of each tic group: subtract \
                tics.append(len(m.group(2)) - 1)
                # Store start of group, end of group, and escape length
                tic_points.append((m.start(2), m.end(2) - 1, 1))
            elif m.group(3):
                # `+
                # Store length of each tic group
                tics.append(len(m.group(3)))
                # Store start of group, end of group, and escape length
                tic_points.append((m.start(3), m.end(3) - 1, 0))
            # Store pipe location
            elif m.group(5):
                pipes.append(m.start(5))

        # Pair up tics according to size if possible
        # Subtract the escape length *only* from the opening.
        # Walk through tic list and see if tic has a close.
        # Store the tic region (start of region, end of region).
        pos = 0
        tic_len = len(tics)
        while pos < tic_len:
            try:
                tic_size = tics[pos] - tic_points[pos][2]
                if tic_size == 0:
                    raise ValueError
                index = tics[pos + 1:].index(tic_size) + 1
                tic_region.append((tic_points[pos][0], tic_points[pos + index][1]))
                pos += index + 1
            except ValueError:
                pos += 1

        # Resolve pipes.  Check if they are within a tic pair region.
        # Walk through pipes comparing them to each region.
        #     - If pipe position is less that a region, it isn't in a region
        #     - If it is within a region, we don't want it, so throw it out
        #     - If we didn't throw it out, it must be a table pipe
        for pipe in pipes:
            throw_out = False
            for region in tic_region:
                if pipe < region[0]:
                    # Pipe is not in a region
                    break
                elif region[0] <= pipe <= region[1]:
                    # Pipe is within a code region.  Throw it out.
                    throw_out = True
                    break
            if not throw_out:
                good_pipes.append(pipe)

        # Split row according to table delimeters.
        pos = 0
        for pipe in good_pipes:
            elements.append(row[pos:pipe])
            pos = pipe + 1
        elements.append(row[pos:])
        return elements


class TableExtension(Extension):
    """ Add tables to Markdown. """

    def extendMarkdown(self, md):
        """ Add an instance of TableProcessor to BlockParser. """
        if '|' not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append('|')
        md.parser.blockprocessors.register(TableProcessor(md.parser), 'tables_extended', 75.1)


def makeExtension(**kwargs):  # pragma: no cover
    return TableExtension(**kwargs)
