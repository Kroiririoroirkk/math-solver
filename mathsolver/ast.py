import fractions


class Expr(object):
    pass


class Lit(Expr):
    def __init__(self, *fraction):
        self.fraction = fractions.Fraction(*fraction)

    def thoroughApply(self, f):
        return f(self)

    def contains(self, e):
        return self == e

    def __eq__(self, other):
        return isinstance(other, Lit) and self.fraction == other.fraction

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.fraction)

    def __repr__(self):
        return 'Lit(fraction=' + repr(self.fraction) + ')'

    def __str__(self, outside=True):
        if self.fraction < 0 and not outside:
            return '(' + str(self.fraction) + ')'
        return str(self.fraction)


class Var(Expr):
    def __init__(self, name):
        self.name = name

    def thoroughApply(self, f):
        return f(self)

    def contains(self, e):
        return self == e

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return 'Var(name=' + repr(self.name) + ')'

    def __str__(self, outside=True):
        return self.name


class Op(Expr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def thoroughApply(self, f):
        if all(e.thoroughApply(f) is None for e in self.args):
            return f(self)
        else:
            return Op(self.name, [e if e.thoroughApply(f) is None
                                  else e.thoroughApply(f)
                                  for e in self.args])

    def contains(self, e):
        if self == e:
            return True
        else:
            return any(subExpr.contains(e) for subExpr in self.args)

    def __eq__(self, other):
        return (isinstance(other, Op)
                and self.name == other.name
                and self.args == other.args)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash((self.name, tuple(self.args)))

    def __repr__(self):
        return 'Op(name=' + repr(self.name) + ', args=' + repr(self.args) + ')'

    def __str__(self, outside=True):
        def prettyFunction():
            return (self.name
                    + '('
                    + ', '.join(e.__str__(outside=False) for e in self.args)
                    + ')')

        def prettyOperator():
            if self.name == '*':
                t = ''
                lits = [e for e in self.args if isinstance(e, Lit)]
                vars = [e for e in self.args if isinstance(e, Var)]
                ops = [e for e in self.args if isinstance(e, Op)]
                if lits:
                    t += ' * '.join(lit.__str__(outside=False) for lit in lits)
                if vars:
                    t += ''.join(var.__str__(outside=False) for var in vars)
                if ops:
                    if t:
                        t += ' * ' + ''.join(op.__str__(outside=False)
                                             for op in ops)
                    else:
                        t += ''.join(op.__str__(outside=False) for op in ops)
                return t
            else:
                opName = ' ' + self.name + ' '
                opArgs = (e.__str__(outside=False) for e in self.args)
                opText = opName.join(opArgs)
                if outside:
                    return opText
                else:
                    return '(' + opText + ')'
        if self.name.isalpha():
            return prettyFunction()
        else:
            return prettyOperator()
