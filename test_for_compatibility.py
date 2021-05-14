
import unittest
from extension_testcase import ExtensionTestCase


class TestExtensionForCompatibility(ExtensionTestCase):
    def test_compatibilty(self):
        self.check_file('testdata/tables.txt', 'testdata/tables.html')


    def test_compatibilty_php(self):
        self.check_file('testdata/tables_php.txt', 'testdata/tables_php.html')


    def test_empty_cells(self):
        """Empty cells (nbsp)."""
        input = """
   | Second Header
------------- | -------------
   | Content Cell
Content Cell  |  
"""
        self.check_text(input, """
                <table>
                <thead>
                <tr>
                <th> </th>
                <th>Second Header</th>
                </tr>
                </thead>
                <tbody>
                <tr>
                <td> </td>
                <td>Content Cell</td>
                </tr>
                <tr>
                <td>Content Cell</td>
                <td> </td>
                </tr>
                </tbody>
                </table>
                """
            )


    def test_cell_row_span(self):
        input = """
| Column 1                | Col 2 | Big row span   |
|:-----------------------:|-------| -------------- |
| r1_c1 spans two cols           || One large cell |
| r2_c1 spans two rows    | r2_c2 |                |
|_^                      _| r3_c2 |                |
|    ______ &#20;         | r4_c2 |_              _|
"""
        self.check_text(input, """
<table>
<thead>
<tr><th align="center">Column 1</th><th>Col 2</th><th>Big row span</th></tr>
</thead>
<tbody>
<tr><td align="center" colspan="2">r1_c1 spans two cols</td><td rowspan="4">One large cell</td></tr>
<tr><td align="center" rowspan="2" valign="top">r2_c1 spans two rows</td><td>r2_c2</td></tr>
<tr><td>r3_c2</td></tr>
<tr><td align="center">______ &#20;</td><td>r4_c2</td></tr>
</tbody>
</table>
""")

if __name__ == '__main__':
    unittest.main()
