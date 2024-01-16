import unittest
from grin import parsing
from main import GrinInterpreter, labelDictionaryCreator


class TestInterpreterJunk(unittest.TestCase):

    def test_junk_class(self):
        letList = list(parsing.parse(
            ['LET A 3', 'LET A 3', 'GOSUB "CHUNK"', 'GOTO "FINAL"', 'CHUNK:  LET A 4', 'LET B 6',
             'RETURN', 'FINAL: LET C 4', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 4)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 6)

if __name__ == '__main__':
    unittest.main()