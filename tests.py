
import unittest
from extension_testcase import ExtensionTestCase


class TestExtension(ExtensionTestCase):
    def test_headerless_table(self):
        input = '''
|----|----|
|r1c1|r1c2|
'''
        self.check_text(input, '''
<table><tbody>
<tr><td>r1c1</td><td>r1c2</td></tr>
</tbody></table>''')
    

    def test_colspan(self):
        input = '''
|----|----|----|
|r1c1    ||r1c3|
'''
        self.check_text(input, '''
<table><tbody>
<tr><td colspan="2">r1c1</td> <td>r1c3</td></tr>
</tbody></table>''')


    def test_rowspan(self):
        input = '''
|----|----|----|
|r1c1|r1c2|r1c3|
|_  _|r2c2|r2c3|
|r3c1|_  _|r3c3|
'''
        self.check_text(input, '''
<table><tbody>
<tr><td rowspan="2">r1c1</td> <td>r1c2</td>             <td>r1c3</td></tr>
<tr>                          <td rowspan="2">r2c2</td> <td>r2c3</td></tr>
<tr><td>r3c1</td>                                       <td>r3c3</td></tr>
</tbody></table>''')


    def test_rowspan_and_colspan(self):
        input = '''
|----|----|----|----|
|r1c1|r1c2|r1c3|r1c4|
|r2c1|r2c2    ||r2c4|
|r3c1|_      _||r3c4|
|r4c1|r4c2|r4c3|r4c4|
'''
        self.check_text(input, '''
<table><tbody>
<tr><td>r1c1</td> <td>r1c2</td>                        <td>r1c3</td> <td>r1c4</td></tr>
<tr><td>r2c1</td> <td colspan="2" rowspan="2">r2c2</td>               <td>r2c4</td></tr>
<tr><td>r3c1</td>                                                    <td>r3c4</td></tr>
<tr><td>r4c1</td> <td>r4c2</td>                        <td>r4c3</td> <td>r4c4</td></tr>
</tbody></table>''')


    def test_valign(self):
        input = '''
|----|----|----|----|
|r1c1|r1c2|r1c3|r1c4|
|____|_^^_|_--_|_==_|
'''
        self.check_text(input, '''
<table><tbody>
<tr>
  <td rowspan="2">r1c1</td>
  <td rowspan="2" valign="top">r1c2</td>
  <td rowspan="2" valign="middle">r1c3</td>
  <td rowspan="2" valign="bottom">r1c4</td>
</tr>
<tr></tr>
</tbody></table>''')


if __name__ == '__main__':
    unittest.main()
