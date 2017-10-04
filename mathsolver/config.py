from enum import Enum

from mathsolver.identities import *
from mathsolver.definitions import *

operators = '+-*/^='

precedence = {
  '^': 4,
  '*': 3,
  '/': 3,
  '+': 2,
  '-': 2,
  '=': 1}

class Associativity(Enum):
  LEFT = 0
  RIGHT = 1

assoc = {
  '^': Associativity.RIGHT,
  '*': Associativity.LEFT,
  '/': Associativity.LEFT,
  '+': Associativity.LEFT,
  '-': Associativity.LEFT,
  '=': Associativity.LEFT}

identities = [commutativePropAddition, groupingPropAddition, zeroIdentityPropAddition, commutativePropMultiplication, groupingPropMultiplication, oneIdentityPropMultiplication, zeroIdentityPropMultiplication, distributivePropExponentiationOverMultiplication, powerOfAPowerProp, zeroToAPowerProp, oneToAPowerProp, toTheFirstPowerProp]

expands = [distributivePropMultiplicationOverAddition]

definitions = [addition, subtraction, negation, multiplication, division, exponentiation, squareRoot, root]

rewriteRules = identities + definitions

expandRules = expands + identities + definitions