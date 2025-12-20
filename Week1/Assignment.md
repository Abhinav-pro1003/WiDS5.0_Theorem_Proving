# Week 1 Assignment: Propositional Logic

This week's assignment focuses on implementing fundamental algorithms for propositional logic: CNF conversion and the DPLL SAT solver. 

## Project Structure

```
Week1/
├── Assignment.md           # This file
├── Plan_Week1.md        
├── prop_logic/
│   ├── to_cnf.py          # CNF conversion (implement this)
│   ├── dpll.py            # DPLL solver (implement this)
│   ├── autograder.py      
│   ├── testcases/        
│      ├── cnf_test_cases.json
│      ├── dpll_test_cases.json
│    
│   
└── fol/  
|   ├── robinson.py  #(implement this)
│   ├── autograder.py     
│   ├── testcases.json   
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

### Test Cases Example
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

# Part 3: First-Order Logic - Robinson's Resolution 

### File: `fol/robinson.py`

Implement the Robinson resolution algorithm for First-Order Logic (FOL). Since FOL satisfiability is undecidable, your implementation should either prove unsatisfiability (UNSAT) or timeout if it cannot determine satisfiability. Also, implement the unification with Most General Unifier (MGU).

### Input Format
- `clauses`: List of clauses in FOL-CNF format
  - Each clause is a list of literals (strings)
  - Variables start with lowercase, predicates/constants with uppercase
  - Example: `["P(x)", "~Q(x, a)"]` represents P(x) ∨ ¬Q(x, a)

### Output Format
- Tuple: `(result: str, proof: list)`
- `result`: Either `"UNSAT"` (unsatisfiable) or `"TIMEOUT"` (undecidable/timeout)
- `proof`: List of resolution steps if UNSAT, empty list if TIMEOUT


### Examples

#### Example 1: Simple UNSAT
```python
# All x: P(x) → Q(x), P(a), ~Q(a)
clauses = [
    ["~P(x)", "Q(x)"],  # P(x) → Q(x)
    ["P(a)"],           # P(a)
    ["~Q(a)"]           # ~Q(a)
]
result, proof = robinson_resolution(clauses, max_iterations=100)
# Output: ("UNSAT", [...resolution steps...])
```

#### Example 2: Satisfiable (Timeout)
```python
# P(a), Q(b) - no contradiction possible
clauses = [
    ["P(a)"],
    ["Q(b)"]
]
result, proof = robinson_resolution(clauses, max_iterations=50)
# Output: ("TIMEOUT", [])
```

## Running the FOL Autograder

```bash
cd Week1/fol
python autograder.py
```

**Good luck with your implementation!**
