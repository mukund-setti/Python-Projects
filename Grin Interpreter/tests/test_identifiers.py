import unittest
from identifiers import Identifiers


class TestIdentifiers(unittest.TestCase):

    def test_setvar_class(self):
        identifierClass = Identifiers()
        identifierClass.setVar('hi', 4)
        self.assertEqual(identifierClass.varDict['hi'], 4)
    def test_getvar_class(self):
        identifierClass = Identifiers()
        identifierClass.setVar('hi', 4)
        result = identifierClass.varDict['hi']
        self.assertEqual(identifierClass.getVar("hi"),  result)
    def test_getvarfalsy_class(self):
        identifierClass = Identifiers()
        identifierClass.setVar('hi', 4)
        result = 0
        self.assertEqual(identifierClass.getVar("huh"),  result)

if __name__ == '__main__':
    unittest.main()