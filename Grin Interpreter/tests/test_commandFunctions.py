import unittest
from io import StringIO
from unittest.mock import patch

import Exceptions
import grin
import main
from commandFunctions import inNumFunction
from grin import parsing
from interpreterjunk import Junk
from main import GrinInterpreter, input_reader, labelDictionaryCreator


class TestCommandFunctions(unittest.TestCase):

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

    def test_div_function_zero(self):
        letList = list(
            parsing.parse(
                ['LET X 5.0', 'DIV X 0', '.']))
        grin_commands = GrinInterpreter(letList, {})
        with self.assertRaises(Exceptions.GrinException) as context:
            grin_commands.run_program()
        self.assertEqual(context.exception.errorMessage,"Cannot divide by zero")

    def test_div_function_str_Str(self):
        letList = list(
            parsing.parse(
                ['LET X "hi"', 'DIV X "hi"', '.']))
        grin_commands = GrinInterpreter(letList, {})
        with self.assertRaises(Exceptions.GrinException) as context:
            grin_commands.run_program()
        self.assertEqual(context.exception.errorMessage, "Cannot divide type str: 'hi' and 'hi'")

    def test_div_function_str_init(self):
        letList = list(
            parsing.parse(
                ['LET X "hi"', 'DIV X 5', '.']))
        grin_commands = GrinInterpreter(letList, {})
        with self.assertRaises(Exceptions.GrinException) as context:
            grin_commands.run_program()
        self.assertEqual(context.exception.errorMessage, "Cannot divide type str: 'hi'")

    def test_div_function_str(self):
        letList = list(
            parsing.parse(
                ['LET X 5', 'DIV X "hi"', '.']))
        grin_commands = GrinInterpreter(letList, {})
        with self.assertRaises(Exceptions.GrinException) as context:
            grin_commands.run_program()
        self.assertEqual(context.exception.errorMessage, "Cannot divide type str: 'hi'")


    def test_div_function_float(self):
        letList = list(parsing.parse(['LET X 5.0', 'DIV X 5.0', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 1.0)

    def test_div_function_float_int(self):
        letList = list(parsing.parse(['LET X 5.0', 'DIV X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 1.0)

    def test_div_function_int_float(self):
        letList = list(parsing.parse(['LET X 5', 'DIV X 5.0', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('X'), 1.0)

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

    def test_conditional(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3<4', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_gt(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 4>3', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_ge(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 5>=4', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_le(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3<=4', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)
    def test_conditional_int_float(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3<4.5', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_equal(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3=3', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_float_int(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3.5<4', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_float_float(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3.0<4.5', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_false(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3>4', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 4)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_conditional_not_equal(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOTO 2 IF 3<>4', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def test_GOSUB_conditional(self):
        letList = list(
            parsing.parse(['LET A 5', 'GOSUB 2 IF 3<>4', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 5)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 3)

    def testGrinException(self):
        letList = list(
            parsing.parse(
                ['LET A 5', 'GOTO 2 IF 3<"4"', 'LET A 4', 'LET B 3', 'END', 'RETURN', '.']))
        grin_commands = GrinInterpreter(letList, {})
        with self.assertRaises(Exceptions.GrinException) as context:
            grin_commands.run_program()
        self.assertEqual(context.exception.errorMessage,
                          "Type <class 'int'> cannot be compared to type <class 'str'>")

    def testInNumFunction(self):
        letList = list(parsing.parse(['INNUM A', '.']))
        user_inputs = '4'
        grin_commands = GrinInterpreter(letList, {})

        with patch('builtins.input', side_effect = user_inputs):
            grin_commands.run_program()
        expected_output = grin_commands.junk.identifiers.varDict['A']
        self.assertEqual(4, expected_output)

    def testInNumFunctionFalsyType(self):
        letList = list(parsing.parse(['INNUM A', '.']))
        user_inputs = 'hi'
        grin_commands = GrinInterpreter(letList, {})
        with self.assertRaises(Exceptions.GrinException) as context:
            with patch('builtins.input', side_effect = user_inputs):
                grin_commands.run_program()
        self.assertEqual(context.exception.errorMessage,"String was inputted, not type int or float")

    def testPrintFunction(self):
        letList = list(parsing.parse(['PRINT "4"', '.']))
        grin_commands = GrinInterpreter(letList, {})
        with patch('sys.stdout', new = StringIO()) as fake_output:
            grin_commands.run_program()
            self.assertEqual(4, int(str(fake_output.getvalue())))
    def testInStrFunction(self):
        letList = list(parsing.parse(['INSTR A', '.']))
        user_inputs = '4'
        grin_commands = GrinInterpreter(letList, {})

        with patch('builtins.input', side_effect = user_inputs):
            grin_commands.run_program()
        expected_output = grin_commands.junk.identifiers.varDict['A']
        self.assertEqual('4', expected_output)

if __name__ == '__main__':
    unittest.main()