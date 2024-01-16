import unittest
from io import StringIO
from unittest.mock import patch

import Exceptions
from Exceptions import GrinException
from grin import parsing
from main import GrinInterpreter, labelDictionaryCreator


class TestExceptions(unittest.TestCase):

    def testGrinException(self):
        letList = list(
            parsing.parse(
                ['LET A 5', 'GOTO 2 IF 3<"4"', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        grin_commands = GrinInterpreter(letList, {})
        with self.assertRaises(Exceptions.GrinException) as context:
            grin_commands.run_program()
        self.assertEqual(context.exception.errorMessage, "Type <class 'int'> cannot be compared to type <class 'str'>")

if __name__ == '__main__':
    unittest.main()