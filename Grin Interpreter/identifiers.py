class Identifiers:
    """
    Represents the identifier manager for Grin variables.

    Attributes:
    - varDict (dict): Dictionary to store variable values.

    Methods:
    - getVar(key: str) -> str|int|float: Retrieves the value of the specified variable.
    - setVar(key: str, value: str|int|float): Sets the value for the specified variable.
    """
    def __init__(self):
        self.varDict = {}

    def getVar(self, key: str) -> str|int|float:
        """
        Retrieve the value of the specified variable.

        Args:
        - key (str): The variable name.

        Returns:
        - str|int|float: The value of the variable if found, otherwise 0.
        """
        if key in self.varDict:
            return self.varDict[key]
        else:
            return 0

    def setVar(self, key: str, value: str|int|float):
        """
        Set the value for the specified variable.

        Args:
        - key (str): The variable name.
        - value (str|int|float): The value to set for the variable.
        """
        self.varDict[key] = value
