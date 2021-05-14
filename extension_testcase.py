import re
import unittest
import markdown

from tables_extended import TableExtension

class ExtensionTestCase(unittest.TestCase):

    def check_text(self, input, expected):
        output = markdown.markdown(input, extensions=[TableExtension()])
        #print(output)
        output = re.sub(r'\s*', '', output)
        expected = re.sub(r'\s*', '', expected)
        self.assertMultiLineEqual(output, expected)


    def check_file(self, infile, outfile):
        with open(infile, encoding="utf-8") as f:
            input = f.read()
        with open(outfile, encoding="utf-8") as f:
            # Normalize line endings
            # (on Windows, git may have altered line endings).
            expected = f.read().replace("\r\n", "\n")
        output = markdown.markdown(input, extensions=[TableExtension()])
        #with open(outfile + ".html", "w", encoding="utf-8") as f:
        #    f.write(output)
        self.assertMultiLineEqual(output, expected)
