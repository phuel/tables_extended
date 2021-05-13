import unittest
import markdown

from tables_extended import TableExtension

class TestExtension(unittest.TestCase):
    def test_compatibilty(self):
        self.__check_file('testdata/tables.txt', 'testdata/tables.html')

    def test_compatibilty_php(self):
        self.__check_file('testdata/tables_php.txt', 'testdata/tables_php.html')

    def __check_file(self, infile, outfile):
        with open(infile, encoding="utf-8") as f:
            input = f.read()
        with open(outfile, encoding="utf-8") as f:
            # Normalize line endings
            # (on Windows, git may have altered line endings).
            expected = f.read().replace("\r\n", "\n")
        output = markdown.markdown(input, extensions=[TableExtension()])
        self.assertMultiLineEqual(output, expected)
