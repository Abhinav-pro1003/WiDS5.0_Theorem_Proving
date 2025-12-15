class Expr:
    pass


class Var(Expr):
    def __init__(self, name):
        self.name = name


class Not(Expr):
    def __init__(self, expr):
        self.expr = expr


class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Or(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right



def to_cnf(expr):
    """
    Converts a propositional logic expression to CNF.
    Returns a list of clauses, each clause is a set of literals.
    """
    raise NotImplementedError