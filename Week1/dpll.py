def inside(variable,dict):
    if "~" in variable:
        if variable[1:] in dict:
            return True
        else:
            return False
    else:
        if variable in dict:
            return True
        else:
            return False

def value_match(variable, dict):
    if not inside(variable,dict):
        return None
    if "~" in variable:
        if dict[variable[1:]]:
            return False
        else:
            return True
    else:
        if dict[variable]:
            return True
        else:
            return False
        
def unit_clause(clauses, assignment):
    while len(clauses)!=0:
        change = False
        add_list = []
        for s in clauses:
            if len(s)==1:
                change = True
                first = next(iter(s))
                if "~" in first:
                    if inside(first,assignment) and not value_match(first,assignment):
                        return 0, clauses, {}
                    assignment[first[1:]] = False
                else:
                    if inside(first,assignment) and not value_match(first,assignment):
                        return 0, clauses, {}
                    assignment[first] = True
            else:
                new_s = set()
                rem = False
                for var in s:
                    if inside(var,assignment):
                        change = True
                        if value_match(var, assignment):
                            rem = True
                            break
                    else:
                        new_s.add(var)
                if rem:
                    pass
                elif len(new_s) == 0:
                    return 0, clauses, {}
                else:
                    add_list.append(new_s)
        clauses = add_list
        if not change:
            break
    if len(clauses)==0:
        return 1, clauses, assignment
    return -1, clauses, assignment

def decision(clauses, assignment, decision_stack):
    for c in clauses:
        for lit in c:
            v = lit[1:] if lit.startswith("~") else lit
            if v not in assignment:
                pick_var = v
                break
        if pick_var is not None:
            break
    if pick_var is None:
        return True, assignment
    for value in (False, True):
        new_stack = set(decision_stack)
        if value:
            new_stack.add("~"+pick_var)
        else:
            new_stack.add(pick_var)
        new_assignment = dict(assignment)
        new_assignment[pick_var] = value

        new_clauses = [set(c) for c in clauses]
        Solve2, reduced_clauses, new_assignment = unit_clause(new_clauses, new_assignment)

        if Solve2 == 1:
            return True, new_assignment
        elif Solve2 == 0:
            clauses.append(set(new_stack))
            continue

        sat, final_assignment = decision(reduced_clauses, new_assignment, new_stack)
        if sat:
            return True, final_assignment
    return False, {}
    

def dpll(clauses, assignment=None):
    """
    clauses: list of sets (e.g. [{'P', '~Q'}, {'Q'}])
    assignment: dict mapping variable -> bool
    Returns: (sat: bool, assignment_or_empty_dict)
    """
    if assignment is None:
        assignment = {}

    Solve, clauses, assignment = unit_clause(clauses, assignment)
    if Solve == 1:
        return True, assignment
    if Solve == 0:
        return False, {}

    decision_stack = set()
    Solve1, final_assignment = decision(clauses, assignment, decision_stack)
    return Solve1, final_assignment