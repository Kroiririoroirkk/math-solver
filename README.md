# math-solver

A simple calculator for manipulating algebraic expressions: it can solve linear and quadratic equations and simplify and expand expressions.

The entry point to the library is `mathsolver.solver`. In the `mathsolver.solver` module, there is:

  * a `stringToAST` function, which takes a `str` and converts it to an `Expr`; it throws a `ValueError` if the input is invalid
  * a `simplifyExpr` function, which takes an `Expr` and simplifies it
  * a `simplifyStr` function, which takes a `str`, converts it into an `Expr`, and then simplifies it; it throws a `ValueError` if the input is invalid
  * an `expandExpr` function, which takes an `Expr` and simplifies it (i.e. simplifies it and applies the distributive property)
  * an `expandStr` function, which takes a `str`, converts it into an `Expr`, and then expands it; it throws a `ValueError` if the input is invalid
  * a `solveLinear` function, which takes a `str` var and an `Expr` e and solves the equation e=0 for var; it returns a `set` with the answer if e is linear in var and `'Expression not linear'` otherwise
  * a `solveQuadratic` function, which takes a `str` var and an `Expr` e and solves the equation e=0 for var; it returns a `set` with the answer(s) if e is quadratic in var and `'Expression not quadratic'` otherwise
  * a `solve` function, which takes a `str` var and an `Expr` e and solves e for var; it returns:

    * a `set` with the answer(s) if e is linear or quadratic in var
    * `'Not an equation'` if e is not an equation
    * `'Equation independent of variable ' + var` if e is independent of var
    * `'Not solvable by this calculator'` if e is neither linear nor quadratic in var

The `demo.py` file contains example usages of these functions.
