from functools import cmp_to_key, reduce

from mathsolver.ast import *

def litsGreatestCmp(e1, e2):
  if isinstance(e1, Lit) and isinstance(e2, Lit):
    if e1.fraction > e2.fraction:
      return 1
    elif e1.fraction == e2.fraction:
      return 0
    else:
      return -1
  elif isinstance(e1, Lit):
    return 1
  elif isinstance(e2, Lit):
    return -1
  elif isinstance(e1, Var) and isinstance(e2, Var):
    if e1.name > e2.name:
      return 1
    elif e1.name == e2.name:
      return 0
    else:
      return -1
  elif isinstance(e1, Var) and (not e2.args):
    return 1
  elif isinstance(e1, Var):
    return litsGreatestCmp(e1, e2.args[0])
  elif isinstance(e1, Op) and isinstance(e2, Op):
    comparedLists = [litsGreatestCmp(e1.args[i], e2.args[i]) for i in range(min(len(e1.args), len(e2.args))) if litsGreatestCmp(e1.args[i], e2.args[i]) != 0]
    if comparedLists:
      return comparedLists[0]
    else:
      return 0
  elif isinstance(e1, Op) and (not e1.args):
    return -1
  else:
    return litsGreatestCmp(e1.args[0], e2)

def commutativePropAddition(e):
  if isinstance(e, Op) and e.name == '+':
    sortedList = sorted(e.args, key=cmp_to_key(litsGreatestCmp))
    if sortedList != e.args:
      return Op('+', sortedList)

def groupingPropAddition(e):
  if isinstance(e, Op) and e.name == '+':
    expandedSumList = reduce(list.__add__,[subExpr.args if isinstance(subExpr, Op) and subExpr.name == '+' else [subExpr] for subExpr in e.args])
    if expandedSumList != e.args:
      return Op('+', expandedSumList)

def zeroIdentityPropAddition(e):
  if isinstance(e, Op) and e.name == '+':
    withoutZeroArgList = list(filter(lambda a: a != Lit(0), e.args))
    if Lit(0) in e.args:
      if withoutZeroArgList[1:]:
        return Op('+', withoutZeroArgList)
      elif withoutZeroArgList:
        return withoutZeroArgList[0]
      else:
        return Lit(0)

def commutativePropMultiplication(e):
  if isinstance(e, Op) and e.name == '*':
    sortedList = sorted(e.args, key=cmp_to_key(litsGreatestCmp))
    if sortedList != e.args:
      return Op('*', sortedList)

def groupingPropMultiplication(e):
  if isinstance(e, Op) and e.name == '*':
    expandedProductList = reduce(list.__add__,[subExpr.args if isinstance(subExpr, Op) and subExpr.name == '*' else [subExpr] for subExpr in e.args])
    if expandedProductList != e.args:
      return Op('*', expandedProductList)

def oneIdentityPropMultiplication(e):
  if isinstance(e, Op) and e.name == '*':
    withoutOneArgList = list(filter(lambda a: a != Lit(1), e.args))
    if Lit(1) in e.args:
      if withoutOneArgList[1:]:
        return Op('*', withoutOneArgList)
      else:
        return withoutOneArgList[0]

def zeroIdentityPropMultiplication(e):
  if isinstance(e, Op) and e.name == '*' and e.args != [Lit(0)] and Lit(0) in e.args:
    return Lit(0)

def distributivePropMultiplicationOverAddition(e):
  if isinstance(e, Op) and e.name == '*':
    try:
      sum = [factor for factor in e.args if isinstance(factor, Op) and factor.name == '+'][0]
      argsWithoutSum = e.args[:]
      argsWithoutSum.remove(sum)
      return Op('+', [Op('*', [summand] + argsWithoutSum) for summand in sum.args])
    except IndexError:
      pass

def distributivePropExponentiationOverMultiplication(e):
  if isinstance(e, Op) and e.name == '^' and len(e.args) == 2 and isinstance(e.args[0], Op) and e.args[0].name == '*':
    return Op('*', [Op('^', [factor, e.args[1]]) for factor in e.args[0].args])

def powerOfAPowerProp(e):
  if isinstance(e, Op) and e.name == '^' and len(e.args) == 2 and isinstance(e.args[0], Op) and e.args[0].name == '^' and len(e.args[0].args) == 2:
    return Op('^', [e.args[0].args[0], Op('*', [e.args[0].args[1], e.args[1]])])
  elif isinstance(e, Op) and e.name == 'root' and len(e.args) == 2 and isinstance(e.args[0], Op) and e.args[0].name == 'root' and len(e.args[0].args) == 2:
    return Op('root', [e.args[0].args[0]], Op('*', [e.args[0].args[1], e.args[1]]))

def zeroToAPowerProp(e):
  if isinstance(e, Op) and (e.name == '^' or e.name == 'root') and e.args[0] == Lit(0) and isinstance(e.args[1], Lit) and e.args[1] != Lit(0):
    return Lit(0)

def oneToAPowerProp(e):
  if isinstance(e, Op) and (e.name == '^' or (e.name == 'root' and isinstance(e.args[1], Lit) and e.args[1] != Lit(0))) and e.args[0] == Lit(1):
    return Lit(1)

def toTheFirstPowerProp(e):
  if isinstance(e, Op) and (e.name == '^' or e.name == 'root') and e.args[1] == Lit(1):
    return e.args[0]