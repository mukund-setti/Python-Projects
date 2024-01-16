from Exceptions import GrinException
from grin import GrinToken, GrinTokenKind
from interpreterjunk import Junk


def letFunction(junk: Junk, line: list[GrinToken]):
    """
    executes let command
    """
    varName = line[1].value()
    varValue = get_token_value(junk, line[2])
    junk.identifiers.setVar(varName, varValue)

def printFunction(junk: Junk, line: list[GrinToken]):
    """
    executes print command
    """
    print(get_token_value(junk, line[1]))

def inNumFunction(junk: Junk, line: list[GrinToken]):
    """
    executes inNum command
    """
    varName = line[1].value()
    varValue = input()
    try:
        typeVarValue = int(varValue)
        junk.identifiers.setVar(varName, typeVarValue)
    except ValueError:
        try:
            # Convert it into float
            typeVarValue = float(varValue)
            junk.identifiers.setVar(varName, typeVarValue)
        except ValueError:
            raise GrinException("String was inputted, not type int or float")

def inStrFunction(junk: Junk, line: list[GrinToken]):
    """
    executes inStr command
    """
    varName = line[1].value()
    varValue = input()
    junk.identifiers.setVar(varName, varValue)

def endFunction(junk: Junk, line: list[GrinToken]):
    """
    executes end command
    """
    junk.currLine.terminateProgram()
def addFunction(junk: Junk, line: list[GrinToken]):
    """
    executes add command
    """
    varName = line[1].value()
    addAmount = get_token_value(junk, line[2])
    varValue = junk.identifiers.getVar(varName)
    if (type(varValue) == str and type(addAmount) != str) or (type(addAmount) == str and type(varValue) != str):
        raise GrinException(f"Can't add type {type(varValue)} and type {type(addAmount)}")
    else:
        newValue = varValue + addAmount
        junk.identifiers.setVar(varName, newValue)

def subFunction(junk: Junk, line: list[GrinToken]):
    """
    executes sub command
    """
    varName = line[1].value()
    subAmount = get_token_value(junk, line[2])
    varValue = junk.identifiers.getVar(varName)
    if type(varValue) == str and type(subAmount) == str:
        raise GrinException(f"Cannot subtract type str: '{subAmount}' from '{varValue}'")
    elif type(varValue) == str:
        raise GrinException(f"Cannot subtract {subAmount} from type str: '{varValue}'")
    elif type(subAmount) == str:
        raise GrinException(f"Cannot subtract type str: '{subAmount}' from {varValue}")
    else:
        newValue = varValue - subAmount
        junk.identifiers.setVar(varName, newValue)
    if type(subAmount) == str:
        raise GrinException("Cannot subtract using string type")
    newValue = varValue - subAmount
    junk.identifiers.setVar(varName, newValue)

def multFunction(junk: Junk, line: list[GrinToken]):
    """
    executes mult command
    """
    varName = line[1].value()
    multAmount = get_token_value(junk, line[2])
    varValue = junk.identifiers.getVar(varName)
    if (type(varValue) == str and type(multAmount) != int) or (type(multAmount) == str and type(varValue) != int):
        raise GrinException(f"Can't multiply type {type(varValue)} and type {type(multAmount)}")
    else:
        newValue = varValue * multAmount
        junk.identifiers.setVar(varName, newValue)


def divFunction(junk: Junk, line: list[GrinToken]):
    """
    executes div command
    """
    varName = line[1].value()
    divAmount = get_token_value(junk, line[2])
    varValue = junk.identifiers.getVar(varName)
    if divAmount == 0:
        raise GrinException("Cannot divide by zero")
    elif type(varValue) == str and type(divAmount) == str:
        raise GrinException(f"Cannot divide type str: '{varValue}' and '{divAmount}'")
    elif type(varValue) == str:
        raise GrinException(f"Cannot divide type str: '{varValue}'")
    elif type(divAmount) == str:
        raise GrinException(f"Cannot divide type str: '{divAmount}'")
    elif type(varValue) == float and type(divAmount) == int:
        newValue = varValue / float(divAmount)
        junk.identifiers.setVar(varName, newValue)
    elif type(varValue) == int and type(divAmount) == float:
        newValue = float(varValue) / divAmount
        junk.identifiers.setVar(varName, newValue)
    elif type(varValue) == int and type(divAmount) == int:
        newValue = varValue / divAmount
        junk.identifiers.setVar(varName, int(newValue))
    elif type(varValue) == float and type(divAmount) == float:
        newValue = varValue / divAmount
        junk.identifiers.setVar(varName, float(newValue))


def goToFunction(junk: Junk, line: list[GrinToken]):
    """
    executes goTo command
    """
    if len(line) == 2:
        to = get_token_value(junk, line[1])
        if type(to) == int:
            currLine = junk.currLine.currLine
            jumpTo = to + currLine
            junk.currLine.jump(jumpTo)
        elif type(to) == str:
            jumpTo = junk.currLine.labelLineNumber(to)
            junk.currLine.jump(jumpTo)
        else:
            raise GrinException(f"Target line isn't a Label or Integer value")
    elif len(line) == 6:
        conditionalInterpretation = evaluateIf(junk, line)
        if conditionalInterpretation:
            to = get_token_value(junk, line[1])
            if type(to) == int:
                currLine = junk.currLine.currLine
                jumpTo = to + currLine
                junk.currLine.jump(jumpTo)
            elif type(to) == str:
                jumpTo = junk.currLine.labelLineNumber(to)
                junk.currLine.jump(jumpTo)
            else:
                raise GrinException(f"Target line isn't a Label or Integer value")
        else:
            junk.currLine.nextLine()


def goSubFunction(junk: Junk, line: list[GrinToken]):
    """
    executes goSub command
    """
    to = get_token_value(junk, line[1])
    if len(line) == 2:
        if type(to) == int:
            currLine = junk.currLine.currLine
            jumpTo = to + currLine
            junk.currLine.jumpRemember(jumpTo)
        elif type(to) == str:
            jumpTo = junk.currLine.labelLineNumber(to)
            junk.currLine.jumpRemember(jumpTo)
        else:
            raise GrinException(f"Target line isn't a Label or Integer value")
    elif len(line) == 6:
        conditionalInterpretation = evaluateIf(junk, line)
        if conditionalInterpretation:
            if type(to) == int:
                currLine = junk.currLine.currLine
                jumpTo = to + currLine
                junk.currLine.jumpRemember(jumpTo)
            elif type(to) == str:
                jumpTo = junk.currLine.labelLineNumber(to)
                junk.currLine.jumpRemember(jumpTo)
            else:
                raise GrinException(f"Target line isn't a Label or Integer value")
        else:
            junk.currLine.nextLine()
def returnFunction(junk: Junk, line: list[GrinToken]):
    """
    executes return command
    """
    junk.currLine.returnToLastCheckpoint()

def get_token_value(junk: Junk, token: GrinToken):
    """
    executes get correct token type
    """
    if token.kind() in (GrinTokenKind.LITERAL_STRING, GrinTokenKind.LITERAL_FLOAT, GrinTokenKind.LITERAL_INTEGER):
        return token.value()
    elif token.kind() == GrinTokenKind.IDENTIFIER:
        return junk.identifiers.getVar(token.value())

def evaluateIf(junk: Junk, line: list[GrinToken]):
    """
    comparison operator logic
    """
    initialComparison = get_token_value(junk, line[3])
    comparedTo = get_token_value(junk, line[5])
    if checkComparisonType(initialComparison, comparedTo):
        if line[4].kind() is GrinTokenKind.EQUAL:
            return initialComparison == comparedTo
        elif line[4].kind() is GrinTokenKind.GREATER_THAN:
            return initialComparison > comparedTo
        elif line[4].kind() is GrinTokenKind.GREATER_THAN_OR_EQUAL:
            return initialComparison >= comparedTo
        elif line[4].kind() is GrinTokenKind.LESS_THAN:
            return initialComparison < comparedTo
        elif line[4].kind() is GrinTokenKind.LESS_THAN_OR_EQUAL:
            return initialComparison <= comparedTo
        elif line[4].kind() is GrinTokenKind.NOT_EQUAL:
            return initialComparison != comparedTo
        else:
            raise GrinException("Not a Valid Comparison Operator")
    else:
        raise GrinException(f"Type {type(initialComparison)} cannot be compared to type {type(comparedTo)}")
def checkComparisonType(initialComparison, comparedTo):
    """
    checks type of objects being compared
    """
    if type(comparedTo) == type(initialComparison):
        return True
    elif type(comparedTo) == int and type(initialComparison) == float:
        return True
    elif type(initialComparison) == int and type(comparedTo) == float:
        return True
    else:
        return False