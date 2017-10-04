from mathsolver.solver import *

print('3x + 3', stringToAST('3x + 3'))
print('boo(1)', stringToAST('boo(1)'))
print('abcf + 8 + 10 + abcf', simplifyStr('abcf + 8 + 10 + abcf'))
print('f((4+x^2)(x^2-7), 6)', expandStr('f((4+x^2)(x^2-7), 6)'))