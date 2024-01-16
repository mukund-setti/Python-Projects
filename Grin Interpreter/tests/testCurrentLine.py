import unittest

import Exceptions
from currentLine import CurrLine
from grin import parsing
from main import GrinInterpreter, labelDictionaryCreator


class TestCurrentLine(unittest.TestCase):

    def test_nextLine_function(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        currLine = CurrLine(len(letList), labelDictionary)
        currLine.nextLine()
        self.assertEqual(currLine.currLine, 2)
    def test_programTerminated_function(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        currLine = CurrLine(len(letList), labelDictionary)
        currLine.currLine = 6
        currLine.totalLines = 5
        self.assertEqual(currLine.programTerminated(), True)
    def test_labelLineNumber_function(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = {"hi":3}
        currLine = CurrLine(len(letList), labelDictionary)
        self.assertEqual(currLine.labelLineNumber("hi"), 3)

    def test_labelLineNumber_function_error(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = {"hi":3}
        currLine = CurrLine(len(letList), labelDictionary)
        with self.assertRaises(Exceptions.GrinException) as context:
            currLine.labelLineNumber("not")
        self.assertEqual(context.exception.errorMessage, "Label not does not exist, cannot jump")

    def testTerminateProgram(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = {"hi": 3}
        currLine = CurrLine(len(letList), labelDictionary)
        currLine.terminateProgram()
        self.assertEqual(currLine.programOver, True)

    def test_jump_function(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        currLine = CurrLine(len(letList), labelDictionary)
        currLine.jump(2)
        self.assertEqual(currLine.currLine, 2)
    def test_jump_error_1(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        currLine = CurrLine(len(letList), labelDictionary)

        with self.assertRaises(Exceptions.GrinException) as context:
            currLine.jump(1)
        self.assertEqual(context.exception.errorMessage, "Cannot jump to current line")

    def test_jump_error_2(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        currLine = CurrLine(len(letList), labelDictionary)

        with self.assertRaises(Exceptions.GrinException) as context:
            currLine.jump(5)
        self.assertEqual(context.exception.errorMessage, "Cannot jump to line past end of program")

    def test_jump_error_3(self):
        letList = list(parsing.parse(['LET X 5', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        currLine = CurrLine(len(letList), labelDictionary)

        with self.assertRaises(Exceptions.GrinException) as context:
            currLine.jump(-5)
        self.assertEqual(context.exception.errorMessage, "Cannot jump to line before program start")

    def test_returnToLastCheckpoint_function(self):
        letList = list(parsing.parse(['LET A 3', 'LET A 3', 'GOSUB "CHUNK"', 'GOTO "FINAL"', 'CHUNK:  LET A 4', 'LET B 6', 'RETURN', 'FINAL: LET C 4', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        grin_commands.run_program()
        self.assertEqual(grin_commands.junk.identifiers.getVar('A'), 4)
        self.assertEqual(grin_commands.junk.identifiers.getVar('B'), 6)

    def test_returnToLastCheckPointError(self):
        letList = list(parsing.parse(
            ['LET A 3', '.']))
        labelDictionary = labelDictionaryCreator(letList)
        grin_commands = GrinInterpreter(letList, labelDictionary)
        with self.assertRaises(Exceptions.GrinException) as context:
            grin_commands.junk.currLine.returnToLastCheckpoint()
        self.assertEqual(context.exception.errorMessage, "Return called with no prior GOSUB call")
if __name__ == '__main__':
    unittest.main()