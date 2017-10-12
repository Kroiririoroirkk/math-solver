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
                intermediateExprs += [rewrite]
                return transformExprRecursive(intermediateExprs, rewrite)
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
        try:
            newList = es[:]
            newList.remove(Var(var))
            newList.append(Lit(1))
            return expandExpr(Op('*', newList))
        except:
            raise ValueError()

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
            if e.name == '*' \
               and all(isinstance(factor, (Lit, Var)) for factor in e.args):
                newList = e.args[:]
                newList.remove(Var(var))
                newList.append(Lit(1))
                return (expandExpr(Op('*', newList)), Lit(0))
            elif e.name == '+':
                varCoefficients = [coefficient(summand)
                                   for summand in e.args
                                   if summand.contains(Var(var))]
                constants = [summand
                             for summand in e.args
                             if not summand.contains(Var(var))]
                if all(varCoefficients):
                    aVal = expandExpr(Op('+', [Lit(0)] + varCoefficients))
                    bVal = expandExpr(Op('+', [Lit(0)] + constants))
                    return (aVal, bVal)
        elif isinstance(e, Var) and e.name == var:
            return (Lit(1), Lit(0))
        raise ValueError()

    def solveLinearWithParts(a, b):
        return {expandExpr(Op('*', [Lit(-1), Op('/', [b, a])]))}
    try:
        return solveLinearWithParts(*getLinearParts())
    except ValueError:
        return 'Expression not linear'


def solveQuadratic(var, e):
    def isVarSquared(expr):
        return expr == Op('^', [Var(var), Lit(2)])

    def divideByVarSquared(es):
        newList = es[:]
        newList = [expr
                   for expr in newList
                   if expr != Var(var) and not isVarSquared(expr)]
        newList.append(Lit(1))
        return expandExpr(Op('*', newList))

    def isQuadraticTerm(expr):
        return isVarSquared(expr) \
               or (isinstance(expr, Op)
                   and expr.name == '*'
                   and any(isVarSquared(factor) for factor in expr.args)
                   and all(isinstance(factor, (Lit, Var))
                           or isVarSquared(factor)
                           for factor in expr.args))

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
        if isVarSquared(e):
            return (Lit(1), Lit(0), Lit(0))
        elif isQuadraticTerm(e):
            return (divideByVarSquared(e.args), Lit(0), Lit(0))
        elif (isinstance(e, Op)
              and e.name == '+'
              and any(isQuadraticTerm(summand) for summand in e.args)):
            varSquaredCoefficients = [coefficient(summand)
                                      for summand in e.args
                                      if isQuadraticTerm(summand)]
            varCoefficients = [coefficient(summand)
                               for summand in e.args
                               if (summand.contains(Var(var))
                                   and not isQuadraticTerm(summand))]
            constants = [summand
                         for summand in e.args
                         if not summand.contains(Var(var))]
            if all(varSquaredCoefficients) and all(varCoefficients):
                aVal = expandExpr(Op('+', [Lit(0)] + varSquaredCoefficients))
                bVal = expandExpr(Op('+', [Lit(0), Lit(0)] + varCoefficients))
                cVal = expandExpr(Op('+', [Lit(0)] + constants))
                return (aVal, bVal, cVal)
        raise ValueError()

    def solveQuadraticWithParts(a, b, c):
        return {expandExpr(solution) for solution in {
            Op('/', [Op('+', [Op('neg', [b]),
                              Op('sqrt',
                                  [Op('-', [Op('^', [b, Lit(2)]),
                                   Op('*', [Lit(4), a, c])])])]),
                     Op('*', [Lit(2), a])]),
            Op('/', [Op('-', [Op('neg', [b]),
                              Op('sqrt',
                                  [Op('-', [Op('^', [b, Lit(2)]),
                                   Op('*', [Lit(4), a, c])])])]),
                     Op('*', [Lit(2), a])])}}
    try:
        return solveQuadraticWithParts(*getQuadraticParts())
    except ValueError:
        return 'Expression not quadratic'


def solve(var, e):
    if isinstance(e, Op) and e.name == '=' and len(e.args) == 2:
        simpleExpr = expandExpr(Op('-', e.args))
    else:
        return 'Not an equation'
    if simpleExpr.contains(Var(var)):
        for solutions in [solveLinear(var, simpleExpr),
                          solveQuadratic(var, simpleExpr)]:
            if isinstance(solutions, set) \
               and all(isinstance(solution, Expr) for solution in solutions):
                return solutions
        else:
            return 'Not solvable by this calculator'
    else:
        return 'Equation independent of variable ' + var


def solveIO():
    equationStr = input('Enter equation: ')
    var = input('Enter variable to solve for: ')
    solutions = solve(var[0], stringToAST(equationStr))
    if isinstance(solutions, str):
        print('Error:', solutions)
    else:
        print('Answer:',
              ', '.join([var[0] + ' = ' + str(solution)
                        for solution in solutions]))
