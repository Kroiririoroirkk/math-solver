import fractions

from mathsolver.ast import *

def reduceThorough(f, es):
  combinations = [(f(es[0], e), e) for e in es[1:] if f(es[0], e) is not None]
  if combinations:
    combination, e2 = combinations[0]
    newList = es[1:]
    newList.remove(e2)
    newList.append(combination)
    return reduceThorough(f, newList)
  else:
    if es[1:]:
      return [es[0]] + reduceThorough(f, es[1:])
    else:
      return [es[0]]

def addExprs(e1, e2):
  if isinstance(e1, Lit) and isinstance(e2, Lit):
    return Lit(e1.fraction + e2.fraction)
  elif isinstance(e1, Op) and e1.name == '*' and len(e1.args) > 1 and isinstance(e2, Op) and e2.name == '*' and len(e2.args) > 1:
    if e1.args[0] == e2.args[0]:
      added = addExprs(e1.args[1] if len(e1.args) == 2 else Op('*', e1.args[1:]), e2.args[1] if len(e2.args) == 2 else Op('*', e2.args[1:]))
      if added:
        return Op('*', [e1.args[0], added])
      else:
        return None
    else:
      return None
  elif isinstance(e1, Op) and e1.name == '*' and len(e1.args) > 1:
    if e1.args[0] == e2:
      added = addExprs(e1.args[1] if len(e1.args) == 2 else Op('*', e1.args[1:]), Lit(1))
      if added:
        return Op('*', [e1.args[0], added])
      else:
        return None
    else:
      return None
  elif isinstance(e2, Op) and e2.name == '*' and len(e2.args) > 1:
    if e1 == e2.args[0]:
      added = addExprs(e2.args[1] if len(e2.args) == 2 else Op('*', e2.args[1:]), Lit(1))
      if added:
        return Op('*', [e2.args[0], added])
      else:
        return None
    else:
      return None
  else:
    if e1 == e2:
      return Op('*', [e1, Lit(2)])
    else:
      return None

def addition(e):
  if isinstance(e, Op) and e.name == '+':
    sumList = reduceThorough(addExprs, e.args)
    if sumList == e.args:
      return None
    else:
      if sumList[1:]:
        return Op('+', sumList)
      else:
        return sumList[0]

def subtraction(e):
  if isinstance(e, Op) and e.name == '-' and len(e.args) == 2:
    return Op('+', [e.args[0], Op('*', [e.args[1], Lit(-1)])])

def negation(e):
  if isinstance(e, Op) and e.name == 'neg' and len(e.args) == 1:
    return Op('*', [e.args[0], Lit(-1)])

def multiplyExprs(e1, e2):
  if isinstance(e1, Lit) and isinstance(e2, Lit):
    return Lit(e1.fraction * e2.fraction)
  elif isinstance(e1, Op) and e1.name == '^' and len(e1.args) == 2 and isinstance(e2, Op) and e2.name == '^' and len(e2.args) == 2:
    if e1.args[0] == e2.args[0]:
      added = addExprs(e1.args[1], e2.args[1])
      if added:
        return Op('^', [e1.args[0], added])
      else:
        return None
    else:
      return None
  elif isinstance(e1, Op) and e1.name == 'root' and len(e1.args) == 2 and isinstance(e2, Op) and e2.name == 'root' and len(e2.args) == 2:
    if e1.args[1] == e2.args[1]:
      return Op('root', [Op('*', [e1.args[0], e2.args[0]]), e1.args[1]])
  elif isinstance(e1, Op) and e1.name == '^' and len(e1.args) == 2:
    if e1.args[0] == e2:
      added = addExprs(e1.args[1], Lit(1))
      if added:
        return Op('^', [e1.args[0], added])
      else:
        return None
    else:
      return None
  elif isinstance(e2, Op) and e2.name == '^' and len(e2.args) == 2:
    if e1 == e2.args[0]:
      added = addExprs(e2.args[1], Lit(1))
      if added:
        return Op('^', [e2.args[0], added])
      else:
        return None
    else:
      return None
  else:
    if e1 == e2:
      return Op('^', [e1, Lit(2)])
    else:
      return None

def multiplication(e):
  if isinstance(e, Op) and e.name == '*':
    productList = reduceThorough(multiplyExprs, e.args)
    if productList == e.args:
      return None
    else:
      if productList[1:]:
        return Op('*', productList)
      else:
        return productList[0]

def division(e):
  if isinstance(e, Op) and e.name == '/' and len(e.args) == 2:
    return Op('*', [e.args[0], Op('^', [e.args[1], Lit(-1)])])

def exponentiation(e):
  if isinstance(e, Op) and e.name == '^' and len(e.args) == 2 and isinstance(e.args[1], Lit):
    if e.args[1].fraction.denominator == 1 and isinstance(e.args[0], Lit):
      return Lit(e.args[0].fraction ** e.args[1].fraction.numerator)
    elif e.args[1].fraction.denominator != 1:
      return Op('root', [Op('^', [e.args[0], e.args[1].fraction.numerator]), Lit(e.args[1].fraction.denominator)])

def squareRoot(e):
  if isinstance(e, Op) and e.name == 'sqrt' and len(e.args) == 1:
    return Op('root', [e.args[0], Lit(2)])

def root(e):
  if isinstance(e, Op) and e.name == 'root' and isinstance(e.args[1], Lit) and e.args[1].fraction.denominator == 1:
    if isinstance(e.args[0], Lit) and e.args[0].fraction.denominator == 1:
      radicand = e.args[0].fraction.numerator
      index = e.args[1].fraction.numerator
      perfectNPowers = ((i**index, i) for i in range(2, radicand))
      val = 1
      for perfectNPower, i in perfectNPowers:
        if perfectNPower > radicand:
          break
        if radicand % perfectNPower == 0:
          radicand /= perfectNPower
          val *= i
      if val != 1:
        return Op('*', [Lit(val), Op('root', [Lit(radicand), Lit(index)])])
    elif isinstance(e.args[0], Op) and e.args[0].name == '^' and isinstance(e.args[0].args[1], Lit):
      var = e.args[0].args[0]
      power = e.args[0].args[1].fraction
      index = e.args[1].fraction.numerator
      resultingPower = 0
      while power > index:
        power -= index
        resultingPower += 1
      if resultingPower:
        if power:
          if index % 2 == 0 and resultingPower % 2 != 0:
            return Op('*', [Op('abs', [Op('^', [var, Lit(resultingPower)])]), Op('root', [Op('^', [var, Lit(power)]), Lit(index)])])
          else:
            return Op('*', [Op('^', [var, Lit(resultingPower)]), Op('root', [Op('^', [var, Lit(power)]), Lit(index)])])
        else:
          if index % 2 == 0 and resultingPower % 2 != 0:
            return Op('abs', [Op('^', [var, Lit(resultingPower)])])
          else:
            return Op('^', [var, Lit(resultingPower)])
    elif isinstance(e.args[0], Op) and e.args[0].name == '*':
      factorList = [root(Op('root', [expr, e.args[1]])) if root(Op('root', [expr, e.args[1]])) else Op('root', [expr, e.args[1]]) for expr in e.args[0].args]
      if [Op('root', [factor, e.args[1]])for factor in e.args[0].args] != factorList:
        return Op('*', factorList)