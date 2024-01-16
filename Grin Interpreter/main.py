import grin
from Exceptions import GrinException
from commandFunctions import letFunction, printFunction, multFunction, divFunction, subFunction, \
    addFunction, returnFunction, goSubFunction, goToFunction, endFunction, inNumFunction, \
    inStrFunction
from currentLine import CurrLine
from grin import GrinTokenKind, GrinParseError, GrinLexError
from identifiers import Identifiers
from interpreterjunk import Junk


def main() -> None:
    """
    Execute the Grin interpreter.

    Read input lines, create a label dictionary, initialize GrinInterpreter, and run the program.
    Handle exceptions and print error messages if encountered.
    """
    try:
        lines = input_reader()
        labelDictionary = labelDictionaryCreator(lines)
        grin_commands = GrinInterpreter(lines, labelDictionary)
        grin_commands.run_program()
    except GrinException as e:
        print(e.errorMessage)
    except GrinParseError as e:
        print(e)
    except GrinLexError as e:
        print(e)


def input_reader():
    """
    Read and process user input lines.

    Read lines from user input until an empty line (or '.') is encountered.
    Parse the lines using the 'grin' package and return the raw lines.
    """
    lines = []

    while True:
        user_input = input()

        # 👇️ if user pressed Enter without a value, break out of loop
        if user_input.strip() == '.':
            break
        else:
            lines.append(user_input)
    rawLines = list(grin.parse(lines))
    return rawLines


def labelDictionaryCreator(rawLines):
    """
    Create a label dictionary from raw lines.

    Create a dictionary mapping labels to line numbers based on the given raw lines.

    Args:
    - rawLines (list): List of raw lines from the input.

    Returns:
    - dict: Label dictionary containing label-to-lineNumber mappings.
    """
    labels = {}
    for line in rawLines:
        if line[0].kind() == GrinTokenKind.IDENTIFIER and line[1].kind() == GrinTokenKind.COLON:
            labels[line[0].value()] = line[0].location().line()
            line.pop(0)
            line.pop(0)
    return labels


class GrinInterpreter:
    """
    Execute the Grin interpreter.

    Handle the execution of Grin program commands based on token types.
    """
    def __init__(self, lines, labelDictionary):
        self.lines = lines
        self.labelDictionary = labelDictionary
        self.junk = Junk(currLine=CurrLine(len(lines), labelDictionary), identifiers=Identifiers())

    def run_program(self):
        """
        Run the Grin program.

        Process each line based on its token kind and call corresponding command functions.
        """
        while not self.junk.currLine.programTerminated():
            currentLine = self.lines[self.junk.currLine.currLine-1]
            if currentLine[0].kind() == GrinTokenKind.LET:
                letFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.PRINT:
                printFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.ADD:
                addFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.SUB:
                subFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.MULT:
                multFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.DIV:
                divFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.GOTO:
                goToFunction(self.junk, currentLine)
            if currentLine[0].kind() == GrinTokenKind.GOSUB:
                goSubFunction(self.junk, currentLine)
            if currentLine[0].kind() == GrinTokenKind.RETURN:
                returnFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.END:
                endFunction(self.junk, currentLine)
            if currentLine[0].kind() == GrinTokenKind.INNUM:
                inNumFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()
            if currentLine[0].kind() == GrinTokenKind.INSTR:
                inStrFunction(self.junk, currentLine)
                self.junk.currLine.nextLine()

if __name__ == '__main__':
    main()
