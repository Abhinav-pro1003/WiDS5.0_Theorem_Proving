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
    Expression = []
    if isinstance(expr, Var):
        Expression.append({expr.name})
        return Expression
    elif isinstance(expr, Not):
        A = expr.expr
        if isinstance(A, Var):
            s = "~" + A.name
            Expression.append({s})
            return Expression
        elif isinstance(A, Not):
            return to_cnf(A.expr)
        elif isinstance(A, And):
            B = Or(Not(A.left), Not(A.right))
            return to_cnf(B)
        elif isinstance(A, Or):
            B = And(Not(A.left), Not(A.right))
            return to_cnf(B)
        elif isinstance(A, Implies):
            B = And(A.left, Not(A.right))
            return to_cnf(B)
    elif isinstance(expr, And):
        A = to_cnf(expr.left)
        for a in A:
            Expression.append(a)
        A = to_cnf(expr.right)
        for a in A:
            Expression.append(a)
        return Expression
    elif isinstance(expr, Or):
        A = to_cnf(expr.left)
        B = to_cnf(expr.right)
        for a in A:
            for b in B:
                Expression.append(a.union(b))
        return Expression
    elif isinstance(expr, Implies):
        B = Or(Not(expr.left), expr.right)
        return to_cnf(B)
    raise NotImplementedError