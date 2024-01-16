from Exceptions import GrinException

class CurrLine:
    """
    Represents the current line control within a program.

    Attributes:
    - currLine (int): Current line number being executed.
    - totalLines (int): Total number of lines in the program.
    - checkpoints (list): List to store checkpoints for GOSUB calls.
    - labelDictionaries (dict): Dictionaries containing label-to-lineNumber mappings.
    - programOver (bool): Indicates whether the program has terminated.

    Methods:
    - programTerminated(): Checks if the program has terminated.
    - terminateProgram(): Marks the program as terminated.
    - nextLine(): Moves to the next line in the program.
    - labelLineNumber(key: str): Retrieves the line number associated with a label.
    - jump(to: int): Jumps execution to the specified line number.
    - jumpRemember(to: int): Jumps execution to a line and remembers the current line.
    - returnToLastCheckpoint(): Returns to the last remembered checkpoint.
    """

    def __init__(self, totalLines: int, labelDictionaries: dict):
        self.currLine = 1
        self.totalLines = totalLines
        self.checkpoints = []
        self.labelDictionaries = labelDictionaries
        self.programOver = False

    def programTerminated(self) -> bool:
        """
        Checks if the program has terminated.

        Returns:
        - bool: True if the program has terminated, False otherwise.
        """
        return self.currLine > self.totalLines or self.programOver

    def terminateProgram(self):
        """Marks the program as terminated."""
        self.programOver = True

    def nextLine(self):
        """Moves to the next line in the program."""
        self.currLine += 1

    def labelLineNumber(self, key: str) -> int:
        """
        Retrieves the line number associated with a label.

        Args:
        - key (str): The label to retrieve line number for.

        Returns:
        - int: The line number associated with the label.

        Raises:
        - GrinException: If the label does not exist.
        """
        if key in self.labelDictionaries:
            return self.labelDictionaries[key]
        else:
            raise GrinException(f"Label {key} does not exist, cannot jump")

    def jump(self, to: int):
        """
        Jumps execution to the specified line number.

        Args:
        - to (int): Line number to jump to.

        Raises:
        - GrinException: If the jump condition is not met.
        """
        if self.currLine == to:
            raise GrinException('Cannot jump to current line')
        elif self.totalLines + 1 < to:
            raise GrinException('Cannot jump to line past end of program')
        elif to <= 0:
            raise GrinException('Cannot jump to line before program start')
        else:
            self.currLine = to

    def jumpRemember(self, to: int):
        """
        Jumps execution to a line and remembers the current line.

        Args:
        - to (int): Line number to jump to.
        """
        self.checkpoints.append(self.currLine)
        self.jump(to)

    def returnToLastCheckpoint(self):
        """
        Returns to the last remembered checkpoint.

        Raises:
        - GrinException: If there are no prior GOSUB calls.
        """
        if len(self.checkpoints) == 0:
            raise GrinException("Return called with no prior GOSUB call")
        else:
            self.jump(self.checkpoints[-1])
            self.checkpoints.pop()
