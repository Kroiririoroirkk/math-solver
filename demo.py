from mathsolver.solver import *

print('3x + 3', stringToAST('3x + 3'), sep='; ')
print('boo(1)', stringToAST('boo(1)'), sep='; ')
try:
  print('3+', stringToAST('3+'), sep='; ')
except ValueError as e:
  print(str(e))
print('abcf + 8 + 10 + abcf', simplifyStr('abcf + 8 + 10 + abcf'), sep='; ')
print('f((4+x^2)(x^2-7), 6)', expandStr('f((4+x^2)(x^2-7), 6)'), sep='; ')
print('x^2+x=fx-3', *solve('x', expandStr('x^2+x=fx-3')), sep='; ')
print('j=5-j', *solve('j', expandStr('j=5-j')), sep='; ')
solveIO()
