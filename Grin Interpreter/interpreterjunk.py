from typing import NamedTuple
from currentLine import CurrLine
from identifiers import Identifiers


class Junk(NamedTuple):
    """
    Prevents circular import, stores instances of class CurrLine and Identifiers
    """
    currLine: CurrLine
    identifiers: Identifiers


