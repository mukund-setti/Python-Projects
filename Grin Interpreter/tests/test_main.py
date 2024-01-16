import unittest
from io import StringIO
from unittest.mock import patch

import grin
import main
from grin import parsing
from main import GrinInterpreter, input_reader, labelDictionaryCreator


class TestProject3(unittest.TestCase):

    def testInputReader(self):
        letList = list(parsing.parse(['PRINT "HI"', '.']))
        user_inputs = ['PRINT "HI"','.']
        grin_commands = GrinInterpreter(letList, {})
        expected_output = "HI\n"
        with patch('builtins.input', side_effect = user_inputs), \
                patch('sys.stdout', new = StringIO()) as fake_output:
            grin_commands.run_program()
            printed_output = fake_output.getvalue()

        # Compare the printed output with the expected output
        self.assertEqual(printed_output, expected_output)

    def testInputReaderCondition1(self):
        # Simulate user input
        user_inputs = [
            'PRINT "HI"',
            '.'
        ]

        with patch('builtins.input', side_effect = user_inputs):
            result = input_reader()

        # Define your expected output based on the input provided
        expected_result = list(parsing.parse(['PRINT "HI"', '.']))

        self.assertEqual(result, expected_result)

    def test_let_function(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 5)
    def test_add_function(self):
        letList = list(parsing.parse(['ADD X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 5)
    def test_sub_function(self):
        letList = list(parsing.parse(['SUB X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), -5)
    def test_div_function(self):
        letList = list(parsing.parse(['DIV X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 0)

    def test_div_function_float(self):
        letList = list(parsing.parse(['LET X 5.0', 'DIV X 5.0', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 1)

    def test_mult_function(self):
        letList = list(parsing.parse(['LET X 2', 'MULT X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 10)

    def test_goSub_function(self):
        letList = list(parsing.parse(['LET A 5', 'GOSUB 2', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_return_function(self):
        letList = list(parsing.parse(['LET A 3', 'LET A 3', 'GOSUB "CHUNK"', 'GOTO "FINAL"', 'CHUNK:  LET A 4', 'LET B 6', 'RETURN', 'FINAL: LET C 4', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 4)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 6)

    def test_goTo_function(self):
        letList = list(parsing.parse(['LET A 5', 'GOTO 2', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)


if __name__ == '__main__':
    unittest.main()