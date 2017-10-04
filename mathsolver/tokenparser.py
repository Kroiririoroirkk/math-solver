from enum import Enum
import fractions

from mathsolver.ast import *
from mathsolver.config import *
from mathsolver.tokenizer import *

def listToAST(tokens):
  def listToASTRecursive(tokens, stack, arityStack, arity, acc):
    def pushToArityStack():
      arityStack.append(1)
    def incrementArityStack():
      if arityStack:
        arityStack.append(arityStack.pop()+1)
    def popArityStack():
      if arityStack:
        nonlocal arity
        arity = arityStack.pop()
    def addLitToResult(s):
      acc.append(Lit(s))
    def addVarToResult(s):
      acc.append(Var(s))
    def pushToStack(s):
      stack.append(s)
    def popUntil(t):
      if stack:
        x = stack.pop()
        if x != t:
          stack.append(x)
          popTopFromStack()
          popUntil(t)
    def popTopFromStack():
      if stack:
        op = stack.pop()
        if op.tokenType == TokenType.OPERATOR:
          try:
            a = acc.pop()
            b = acc.pop()
            acc.append(Op(op.content, [b,a]))
          except IndexError:
            raise ValueError('Invalid input')
        elif op.tokenType == TokenType.FUNCTION:
          popArityStack()
          nonlocal arity
          try:
            args = [acc.pop() for i in range(arity)]
          except IndexError:
            raise ValueError('Invalid input')
          arity = 0
          acc.append(Op(op.content, args[::-1]))
    def popAllFromStack():
      if stack:
        popTopFromStack()
        popAllFromStack()
    def popOperatorsFromStack(c):
      if stack:
        op = stack.pop()
        stack.append(op)
        if op.tokenType == TokenType.OPERATOR:
          if assoc[c] == Associativity.LEFT and precedence[op.content] >= precedence[c]:
            popTopFromStack()
            popOperatorsFromStack(c)
          elif assoc[c] == Associativity.RIGHT and precedence[op.content] > precedence[c]:
            popTopFromStack()
            popOperatorsFromStack(c)
        elif op.tokenType == TokenType.FUNCTION:
          popTopFromStack()
          popOperatorsFromStack(c)
    def fromToken(t):
      if t.tokenType == TokenType.LITERAL:
        addLitToResult(t.content)
      elif t.tokenType == TokenType.VARIABLE:
        addVarToResult(t.content)
      elif t.tokenType == TokenType.FUNCTION:
        pushToStack(t)
        pushToArityStack()
      elif t.tokenType == TokenType.OPERATOR:
        popOperatorsFromStack(t.content[0])
        pushToStack(t)
      elif t.tokenType == TokenType.COMMA:
        popUntil(Token(TokenType.LPARENTHESIS, '('))
        pushToStack(Token(TokenType.LPARENTHESIS, '('))
        incrementArityStack()
      elif t.tokenType == TokenType.LPARENTHESIS:
        pushToStack(t)
      elif t.tokenType == TokenType.RPARENTHESIS:
        popUntil(Token(TokenType.LPARENTHESIS, '('))
    if tokens:
      fromToken(tokens[0])
      return listToASTRecursive(tokens[1:], stack, arityStack, arity, acc)
    else:
      popAllFromStack()
      if not acc or acc[1:]:
        raise ValueError('Invalid input')
      else:
        return acc[0]
  return listToASTRecursive(tokens, [], [], 0, [])