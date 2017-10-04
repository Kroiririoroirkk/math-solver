from mathsolver.ast import *
from mathsolver.config import *
from mathsolver.tokenparser import *

def stringToAST(s):
  try:
    return listToAST(tokenize(s))
  except ValueError:
    raise

def transformExpr(rules, e):
  def firstRewrite(expr):
    for maybeExpr in [expr.thoroughApply(rule) for rule in rules]:
      if maybeExpr:
        return maybeExpr
    return None
  def transformExprRecursive(intermediateExprs, expr):
    rewrite = firstRewrite(expr)
    if rewrite in intermediateExprs:
      return expr
    else:
      if rewrite:
        return transformExprRecursive(intermediateExprs + [rewrite], rewrite)
      else:
        return expr
  return transformExprRecursive([], e)

def simplifyExpr(e):
  return transformExpr(rewriteRules, e)

def simplifyStr(s):
  try:
    return simplifyExpr(stringToAST(s))
  except ValueError:
    return None

def expandExpr(e):
  return transformExpr(expandRules, e)

def expandStr(s):
  try:
    return expandExpr(stringToAST(s))
  except ValueError:
    return None

def solveLinear(var, e):
  def divideByVar(es):
    newList = es[:]
    newList.remove(Var(var))
    newList.append(Lit(1))
    return expandExpr(Op('*', newList))
  def coefficient(term):
    if isinstance(term, Lit):
      return None
    elif isinstance(term, Var):
      if term == Var(var):
        return Lit(1)
      else:
        return None
    elif isinstance(term, Op) and term.name == '*':
      if divideByVar(term.args).contains(Var(var)):
        return None
      else:
        return divideByVar(term.args)
    else:
      return None
  def getLinearParts():
    if isinstance(e, Op):
      if e.name == '*' and all([isinstance(factor, Lit) or isinstance(factor, Var) for factor in e.args]):
        newList = e.args[:]
        newList.remove(Var(var))
        newList.append(Lit(1))
        return (expandExpr(Op('*', newList)), Lit(0))
      elif e.name == '+':
        varCoefficients = [coefficient(summand) for summand in e.args if summand.contains(Var(var))]
        if all(varCoefficients):
          aVal = expandExpr(Op('+', [Lit(0)] + varCoefficients))
          bVal = expandExpr(Op('+', [Lit(0)] + [summand for summand in e.args if not summand.contains(Var(var))]))
          return (aVal, bVal)
    elif isinstance(e, Var) and e.name == var:
      return (Lit(1), Lit(0))
  def solveLinearWithParts(a, b):
    return {expandExpr(Op('*', [Lit(-1), Op('/', [b, a])]))}
  linearParts = getLinearParts()
  if linearParts:
    return solveLinearWithParts(*linearParts)
  else:
    return 'Expression not linear'

def solveQuadratic(var, e):
  def divideByVarSquared(es):
    newList = es[:]
    newList = [expr for expr in newList if expr != Var(var) and expr != Op('^', [Var(var), Lit(2)])]
    newList.append(Lit(1))
    return expandExpr(Op('*', newList))
  def isQuadraticTerm(expr):
    return isinstance(expr, Op) and expr.name == '^' and expr.args == [Var(var), Lit(2)]
  def coefficient(term):
    if isinstance(term, Lit):
      return None
    elif isinstance(term, Var):
      if term == Var(var):
        return Lit(1)
      else:
        return None
    elif isinstance(term, Op) and term.name == '*':
      if divideByVarSquared(term.args).contains(Var(var)):
        return None
      else:
        return divideByVarSquared(term.args)
    elif isQuadraticTerm(term):
      return Lit(1)
    else:
      return None
  def getQuadraticParts():
    if isinstance(e, Op):
      if e.name == '^' and e.args == [Var(var), Lit(2)]:
        return (Lit(1), Lit(0), Lit(0))
      elif e.name == '*' and all([isinstance(factor, Lit) or isinstance(factor, Var) or isQuadraticTerm(factor) for factor in e.args]):
        return (divideByVarSquared(e.args), Lit(0), Lit(0))
      elif e.name == '+' and any([summand.contains(Op('^', [Var(var), Lit(2)])) for summand in e.args]):
        varSquaredCoefficients = [coefficient(summand) for summand in e.args if isQuadraticTerm(summand)]
        varCoefficients = [coefficient(summand) for summand in e.args if summand.contains(Var(var)) and not isQuadraticTerm(summand)]
        if all(varSquaredCoefficients) and all(varCoefficients):
          aVal = expandExpr(Op('+', [Lit(0)] + varSquaredCoefficients))
          bVal = expandExpr(Op('+', [Lit(0), Lit(0)] + varCoefficients))
          cVal = expandExpr(Op('+', [Lit(0)] + [summand for summand in e.args if not summand.contains(Var(var))]))
          return (aVal, bVal, cVal)
  def solveQuadraticWithParts(a, b, c):
    return {expandExpr(solution) for solution in {
      Op('/', [Op('+', [Op('neg', [b]), Op('sqrt', [Op('-', [Op('^', [b, Lit(2)]), Op('*', [Lit(4), a, c])])])]), Op('*', [Lit(2), a])]),
      Op('/', [Op('-', [Op('neg', [b]), Op('sqrt', [Op('-', [Op('^', [b, Lit(2)]), Op('*', [Lit(4), a, c])])])]), Op('*', [Lit(2), a])])}}
  quadraticParts = getQuadraticParts()
  if quadraticParts:
    return solveQuadraticWithParts(*quadraticParts)
  else:
    return 'Expression not quadratic'

def solve(var, e):
  if isinstance(e, Op) and e.name == '=' and len(e.args) == 2:
    simpleExpr = expandExpr(Op('-', e.args))
  else:
    return 'Not an equation'
  if simpleExpr.contains(Var(var)):
    try:
      return [exprs for exprs in [
        solveLinear(var, simpleExpr),
        solveQuadratic(var, simpleExpr)
      ] if all([isinstance(expr, Expr) for expr in exprs])][0]
    except IndexError:
      return 'Not solvable by this calculator'
  else:
    return 'Equation independent of variable ' + var

def solveIO():
  equationStr = input('Enter equation: ')
  var = input('Enter variable to solve for: ')
  solutions = solve(var, stringToAST(equationStr))
  if isinstance(solutions, str):
    print('Error:', solutions)
  else:
    print('Answer:', ', '.join([var + ' = ' + str(solution) for solution in solutions]))