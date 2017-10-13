from collections import namedtuple
from enum import Enum

from mathsolver.config import operators


class TokenType(Enum):
    LITERAL = 0
    VARIABLE = 1
    FUNCTION = 2
    OPERATOR = 3
    COMMA = 4
    LPARENTHESIS = 5
    RPARENTHESIS = 6

Token = namedtuple('Token', ['tokenType', 'content'])


def tokenize(s):
    def tokenizeRecursive(s, literalBuffer, letterBuffer, acc):
        def addToResult(t):
            acc.append(t)

        def addToLiteralBuffer(c):
            literalBuffer.append(c)

        def emptyLiteralBuffer():
            nonlocal literalBuffer
            if literalBuffer:
                acc.append(Token(TokenType.LITERAL, ''.join(literalBuffer)))
                literalBuffer = []

        def addToLetterBuffer(c):
            letterBuffer.append(c)

        def emptyLetterBufferAsFunction():
            nonlocal letterBuffer
            addToResult(Token(TokenType.FUNCTION, ''.join(letterBuffer)))
            letterBuffer = []

        def emptyLetterBufferAsVariables():
            nonlocal acc, letterBuffer

            def intersperse(seq, value):
                res = [value] * (2 * len(seq) - 1)
                res[::2] = seq
                return res
            acc += intersperse([Token(TokenType.VARIABLE, letter)
                                for letter in letterBuffer],
                               Token(TokenType.OPERATOR, '*'))
            letterBuffer = []

        def toToken(c):
            if c.isdecimal() or c == '.':
                addToLiteralBuffer(c)
            elif c.isalpha():
                if literalBuffer:
                    emptyLiteralBuffer()
                    addToResult(Token(TokenType.OPERATOR, '*'))
                addToLetterBuffer(c)
            elif c in operators:
                emptyLiteralBuffer()
                emptyLetterBufferAsVariables()
                addToResult(Token(TokenType.OPERATOR, c))
            elif c == ',':
                emptyLiteralBuffer()
                emptyLetterBufferAsVariables()
                addToResult(Token(TokenType.COMMA, c))
            elif c == '(':
                if letterBuffer:
                    emptyLetterBufferAsFunction()
                elif literalBuffer:
                    emptyLiteralBuffer()
                    addToResult(Token(TokenType.OPERATOR, '*'))
                nonlocal acc
                if acc and acc[-1] == Token(TokenType.RPARENTHESIS, ')'):
                    addToResult(Token(TokenType.OPERATOR, '*'))
                addToResult(Token(TokenType.LPARENTHESIS, '('))
            elif c == ')':
                emptyLiteralBuffer()
                emptyLetterBufferAsVariables()
                addToResult(Token(TokenType.RPARENTHESIS, ')'))
        if s:
            toToken(s[0])
            return tokenizeRecursive(s[1:], literalBuffer, letterBuffer, acc)
        else:
            emptyLiteralBuffer()
            emptyLetterBufferAsVariables()
            return acc
    return tokenizeRecursive(s, [], [], [])
