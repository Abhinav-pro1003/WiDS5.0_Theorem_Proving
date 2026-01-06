"""
First-Order Logic - Robinson's Resolution Algorithm
Implement the Robinson resolution algorithm for FOL theorem proving.
"""

from typing import List, Tuple

def is_variable(t: str) -> bool:
    return t.islower()

def parse_literal(lit: str):
    neg = lit.startswith("~")
    lit = lit[1:] if neg else lit

    if "(" not in lit:
        return neg, lit, []

    i = lit.find("(")
    name = lit[:i]
    inside = lit[i+1:-1]   # remove outer brackets

    args = []
    depth = 0
    current = ""

    for ch in inside:
        if ch == "," and depth == 0:
            args.append(current)
            current = ""
        else:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            current += ch

    if current:
        args.append(current)

    return neg, name, args

def apply_subs(term: str, subs: dict):
    if term in subs:
        return subs[term]

    if "(" not in term:
        return term

    i = term.find("(")
    name = term[:i]
    inside = term[i+1:-1]
    args = []
    depth = 0
    cur = ""

    for ch in inside:
        if ch == "," and depth == 0:
            args.append(apply_subs(cur, subs))
            cur = ""
        else:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            cur += ch

    if cur:
        args.append(apply_subs(cur, subs))

    return name + "(" + ",".join(args) + ")"

def unify_terms(t1, t2, subs):
    t1 = apply_subs(t1, subs)
    t2 = apply_subs(t2, subs)

    if t1 == t2:
        return subs

    if is_variable(t1):
        if t1 in t2:
            return None
        subs[t1] = t2
        return subs

    if is_variable(t2):
        if t2 in t1:
            return None
        subs[t2] = t1
        return subs

    if "(" in t1 and "(" in t2:
        n1, f1, a1 = parse_literal(t1)
        n2, f2, a2 = parse_literal(t2)
        if f1 != f2 or len(a1) != len(a2):
            return None
        for x, y in zip(a1, a2):
            subs = unify_terms(x, y, subs)
            if subs is None:
                return None
        return subs

    return None

def is_complement(l1, l2):
    n1, p1, a1 = parse_literal(l1)
    n2, p2, a2 = parse_literal(l2)

    return (
        p1 == p2 and
        len(a1) == len(a2) and
        n1 != n2
    )

def unify(lit1: str, lit2: str) -> dict:
    """
    Unification algorithm - find most general unifier (MGU).
    
    Returns:
        Substitution dictionary if unifiable, None otherwise
    """
    # TODO: Implement unification algorithm
    neg1, p1, args1 = parse_literal(lit1)
    neg2, p2, args2 = parse_literal(lit2)

    if p1 != p2 or len(args1) != len(args2):
        return None

    subs = {}
    for a, b in zip(args1, args2):
        subs = unify_terms(a, b, subs)
        if subs is None:
            return None
    return subs

    pass

def robinson_resolution(clauses: List[List[str]], max_iterations: int = 1000) -> Tuple[str, List]:
    """
    Robinson's resolution algorithm for FOL.
    
    Args:
        clauses: List of clauses in CNF (each clause is list of literals)
        max_iterations: Maximum resolution steps before timeout
        
    Returns:
        ("UNSAT", proof) if empty clause derived (contradiction found)
        ("TIMEOUT", []) if max_iterations reached or no new clauses
    """
    # TODO: Implement Robinson's resolution algorithm
    clauses = [set(c) for c in clauses]
    proof = []
    seen = {frozenset(c) for c in clauses}

    for _ in range(max_iterations):
        new_clauses = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                c1, c2 = clauses[i], clauses[j]

                for l1 in c1:
                    for l2 in c2:
                        if not is_complement(l1,l2):
                            continue

                        subs = unify(l1, l2)
                        if subs is None:
                            continue

                        resolvent = set()
                        for l in c1:
                            if l != l1:
                                resolvent.add(apply_subs(l, subs))
                        for l in c2:
                            if l != l2:
                                resolvent.add(apply_subs(l, subs))

                        if not resolvent:
                            return "UNSAT", proof
                        key = frozenset(resolvent)
                        if key not in seen:
                            seen.add(key)
                            new_clauses.append(resolvent)
                            proof.append((clauses[i], clauses[j], resolvent))

        if not new_clauses:
            return "TIMEOUT", []

        clauses.extend(new_clauses)

    return "TIMEOUT", []

    pass
