# Week 1: Introduction to Foundations of Logic and The Logic Theorist
Welcome to Week 1! We will cover the foundations of Logic and Inference and Proof systems. We will also get an introduction to the Logic Theorist which has been described as the first Artificial Intelligence Program.

## Recommended Resources

### **Read / Watch**
- *Logic in Computer Science* — Huth & Ryan (Ch. 1–2 for propositional logic)  
- *Artificial Intelligence: A Modern Approach* — Russell & Norvig (Ch. 7 & 8)  
- *The Logic Theorist: A Machine That Proves Theorems* — Newell & Simon (1956)
- A Nice Introduction to the Contribution of The Logic Theorist: [The Logic Theorist Wikipedia Page](https://en.wikipedia.org/wiki/Logic_Theorist)
- **YouTube**:  
  - [Computerphile – Logic Gates and Propositional Logic](https://www.youtube.com/watch?v=w3F-N7UFP0w)  
  - [ColdFusion – The First AI Program: Logic Theorist](https://www.youtube.com/watch?v=yaN5w2kAG8k)

### **Practice / Tools**
- [logictools.org](https://logictools.org) — truth tables & logic proofs online  
- [PyEDA](https://pyeda.readthedocs.io/en/latest/) — Python package for Boolean logic manipulation  
- [Tarski](https://tarski.readthedocs.io/en/latest/) — logic & model-checking toolkit  


## Extending Week-1 

### Objective
- Understand First-Order Logic (predicates, functions, quantifiers) and Robinson's resolution algorithm
- Learn unification with Most General Unifier (MGU) and occurs check
- Understand why FOL is undecidable and how to handle timeouts

### Implementation
- Complete FOL theorem prover in `fol/robinson.py`
- Run `python3 autograder.py` in `Week1/fol/` to test (15 test cases: UNSAT/TIMEOUT)

### References
- *Logic in Computer Science* — Huth & Ryan (Ch. 3)
- *AI: A Modern Approach* — Russell & Norvig (Ch. 9)
- [Robinson's Resolution Paper](https://www.cip.ifi.lmu.de/~sprinz/sprinz_2021_unification.pdf)
- [SWI-Prolog](https://www.swi-prolog.org/) — Try logic programming in practice
