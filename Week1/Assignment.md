# Week 1 Assignment: Propositional Logic

This week's assignment focuses on implementing fundamental algorithms for propositional logic: CNF conversion and the DPLL SAT solver. 

## Project Structure

```
Week1/
├── Assignment.md           # This file
├── Plan_Week1.md          # Weekly learning plan
├── prop_logic/
│   ├── to_cnf.py          # CNF conversion (implement this)
│   ├── dpll.py            # DPLL solver (implement this)
│   ├── autograder.py      # Automated testing script
│   ├── testcases/         # Test cases directory
│      ├── cnf_test_cases.json
│      ├── dpll_test_cases.json
│    
│   
└── fol/              
```

## Part 1: CNF Conversion (15 test cases)

### File: `prop_logic/to_cnf.py`

Implement the `to_cnf(expr)` function that converts a propositional logic expression to Conjunctive Normal Form.

### Input Format
- Expression tree using classes: `Var`, `Not`, `And`, `Or`, `Implies`
- Example: `Implies(Var("P"), Var("Q"))` represents P → Q

### Output Format
- List of clauses, where each clause is a set of literals
- Example: `[{'~P', 'Q'}]` for P → Q


### Example
```python
# Input: P -> Q
expr = Implies(Var("P"), Var("Q"))
result = to_cnf(expr)
# Output: [{'~P', 'Q'}]

# Input: ~(P & Q)
expr = Not(And(Var("P"), Var("Q")))
result = to_cnf(expr)
# Output: [{'~P', '~Q'}]

# Input: P | (Q & R)
expr = Or(Var("P"), And(Var("Q"), Var("R")))
result = to_cnf(expr)
# Output: [{'P', 'Q'}, {'P', 'R'}]
```

## Part 2: DPLL SAT Solver (15 test cases)

### File: `prop_logic/dpll.py`

Implement the `dpll(clauses, assignment)` function that determines if a CNF formula is satisfiable.

### Input Format
- `clauses`: List of sets representing CNF clauses
  - Example: `[{'P', '~Q'}, {'Q'}]`
- `assignment`: Dictionary mapping variables to boolean values (optional)

### Output Format
- Tuple: `(satisfiable: bool, assignment: dict)`
- `satisfiable`: True if formula is satisfiable, False otherwise
- `assignment`: A satisfying assignment if SAT, empty dict if UNSAT

### Test Cases
- **Basic (5 tests)**: Empty clauses, unit clauses, simple contradictions
- **Medium (5 tests)**: Unit propagation, pure literals, simple formulas
- **Hard (5 tests)**: 3-SAT problems, complex formulas, pigeonhole principle

### Example
```python
# Satisfiable formula
clauses = [{'P', 'Q'}, {'~P', 'Q'}]
sat, assignment = dpll(clauses)
# Output: (True, {'Q': True})

# Unsatisfiable formula
clauses = [{'P'}, {'~P'}]
sat, assignment = dpll(clauses)
# Output: (False, {})

# Unit propagation example
clauses = [{'P'}, {'~P', 'Q'}, {'~Q', 'R'}]
sat, assignment = dpll(clauses)
# Output: (True, {'P': True, 'Q': True, 'R': True})
```

## Running the Autograder

### Prerequisites
- Python 3.6 or higher
- Standard library only (don't use external dependencies)

### Usage
```bash
cd Week1/prop_logic
python autograder.py
```

## Submission Guidelines
1. Implement your solutions in `to_cnf.py` and `dpll.py`
2. Test thoroughly using the autograder
3. Ensure all imports and class definitions remain unchanged


## Resources
### CNF Conversion
- [CNF on Wikipedia](https://en.wikipedia.org/wiki/Conjunctive_normal_form)

### DPLL Algorithm
- [DPLL on Wikipedia](https://en.wikipedia.org/wiki/DPLL_algorithm)
- Davis-Putnam-Logemann-Loveland algorithm
- Unit propagation and pure literal elimination
---

**Good luck with your implementation! Remember: automated theorem proving is a powerful tool for verifying complex systems.**
