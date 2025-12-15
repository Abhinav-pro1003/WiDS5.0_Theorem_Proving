def dpll(clauses, assignment=None):
    """
    clauses: list of sets (e.g. {{'P', '~Q'}, {'Q'}})
    assignment: dict mapping variable -> bool
    Returns: (sat: bool, assignment)
    """
    if assignment is None:
        assignment = {}

    raise NotImplementedError