from mathsolver.solver import *

print('3x + 3', stringToAST('3x + 3'), sep='; ')
print('boo(1)', stringToAST('boo(1)'), sep='; ')
try:
    print('3+', stringToAST('3+'), sep='; ')
except ValueError as e:
    print(str(e))
print('abcf + 8 + 10 + abcf', simplifyStr('abcf + 8 + 10 + abcf'), sep='; ')
print('abcf + 8 + 10 + abcf', simplifyExpr(stringToAST('abcf + 8 + 10 + abcf')), sep='; ')
print('f((4+x^2)(x^2-7), 6)', expandStr('f((4+x^2)(x^2-7), 6)'), sep='; ')
print('f((4+x^2)(x^2-7), 6)', expandExpr(stringToAST('f((4+x^2)(x^2-7), 6)')), sep='; ')
print('x+1=3-p', *solveLinear('p', stringToAST('x+1=3-p')))
print('x^2+x=6(x-7)', *solveQuadratic('p', expandStr('x^2+x=6(x-7)')))
print('x^2+x=fx-3', *solve('x', expandStr('x^2+x=fx-3')), sep='; ')
print('j=5-j', *solve('j', expandStr('j=5-j')), sep='; ')


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


solveIO()
