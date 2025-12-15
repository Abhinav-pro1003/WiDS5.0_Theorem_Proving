"""
Autograder for Propositional Logic Assignment
Tests both to_cnf.py and dpll.py implementations
"""

import json
import os
import sys
from typing import List, Set, Dict, Tuple, Any
import traceback

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the modules to test
try:
    from to_cnf import Expr, Var, Not, And, Or, Implies, to_cnf
    CNF_IMPORT_SUCCESS = True
except Exception as e:
    print(f"Error importing to_cnf.py: {e}")
    CNF_IMPORT_SUCCESS = False
    Expr = Var = Not = And = Or = Implies = to_cnf = None

try:
    from dpll import dpll
    DPLL_IMPORT_SUCCESS = True
except Exception as e:
    print(f"Error importing dpll.py: {e}")
    DPLL_IMPORT_SUCCESS = False
    dpll = None


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


def parse_expression(expr_str: str) -> Expr:
    """
    Parse a string representation of a propositional logic expression.
    Supports: P, ~P, P & Q, P | Q, P -> Q, parentheses
    """
    expr_str = expr_str.strip()
    
    # Handle parentheses
    if expr_str.startswith('(') and expr_str.endswith(')'):
        # Find matching closing parenthesis
        depth = 0
        for i, char in enumerate(expr_str):
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            if depth == 0 and i == len(expr_str) - 1:
                return parse_expression(expr_str[1:-1])
    
    # Find main operator (lowest precedence first)
    # Precedence: -> (lowest), |, &, ~ (highest)
    
    # Look for -> (implication)
    depth = 0
    for i in range(len(expr_str) - 1, -1, -1):
        if expr_str[i] == '(':
            depth += 1
        elif expr_str[i] == ')':
            depth -= 1
        elif depth == 0 and i > 0 and expr_str[i-1:i+1] == '->':
            left = parse_expression(expr_str[:i-1].strip())
            right = parse_expression(expr_str[i+1:].strip())
            return Implies(left, right)
    
    # Look for | (or)
    depth = 0
    for i in range(len(expr_str) - 1, -1, -1):
        if expr_str[i] == '(':
            depth += 1
        elif expr_str[i] == ')':
            depth -= 1
        elif depth == 0 and expr_str[i] == '|':
            left = parse_expression(expr_str[:i].strip())
            right = parse_expression(expr_str[i+1:].strip())
            return Or(left, right)
    
    # Look for & (and)
    depth = 0
    for i in range(len(expr_str) - 1, -1, -1):
        if expr_str[i] == '(':
            depth += 1
        elif expr_str[i] == ')':
            depth -= 1
        elif depth == 0 and expr_str[i] == '&':
            left = parse_expression(expr_str[:i].strip())
            right = parse_expression(expr_str[i+1:].strip())
            return And(left, right)
    
    # Handle negation
    if expr_str.startswith('~'):
        inner = parse_expression(expr_str[1:].strip())
        return Not(inner)
    
    # Base case: variable
    return Var(expr_str)


def normalize_cnf(cnf: Any) -> List[Set[str]]:
    """
    Normalize CNF to a list of sets of literals for comparison.
    Handles various possible return formats from to_cnf.
    """
    if isinstance(cnf, list):
        result = []
        for clause in cnf:
            if isinstance(clause, set):
                result.append(clause)
            elif isinstance(clause, list):
                result.append(set(clause))
            else:
                result.append({str(clause)})
        return sorted([sorted(list(clause)) for clause in result])
    return []


def cnf_equals(cnf1: List[Set[str]], cnf2: List[Set[str]]) -> bool:
    """Check if two CNF formulas are equivalent (same clauses)."""
    norm1 = sorted([sorted(list(clause)) for clause in cnf1])
    norm2 = sorted([sorted(list(clause)) for clause in cnf2])
    return norm1 == norm2


def verify_dpll_assignment(clauses: List[List[str]], assignment: Dict[str, bool]) -> bool:
    """Verify that an assignment satisfies all clauses."""
    for clause in clauses:
        satisfied = False
        for literal in clause:
            if literal.startswith('~'):
                var = literal[1:]
                if var in assignment and not assignment[var]:
                    satisfied = True
                    break
            else:
                var = literal
                if var in assignment and assignment[var]:
                    satisfied = True
                    break
        if not satisfied:
            return False
    return True


def test_to_cnf(test_cases: List[Dict]) -> Tuple[int, List[Dict]]:
    """
    Test the to_cnf function with given test cases.
    Returns: (passed_count, results)
    """
    if not CNF_IMPORT_SUCCESS:
        return 0, []
    
    passed = 0
    results = []
    
    for test_case in test_cases:
        result = {
            'id': test_case['id'],
            'description': test_case['description'],
            'passed': False,
            'error': None
        }
        
        try:
            # Parse input expression
            expr = parse_expression(test_case['input'])
            
            # Call to_cnf
            cnf_output = to_cnf(expr)
            
            # Normalize both expected and actual output
            expected = [set(clause) for clause in test_case['expected']]
            actual = normalize_cnf(cnf_output)
            expected_norm = normalize_cnf(expected)
            
            # Compare
            if cnf_equals(expected, actual):
                result['passed'] = True
                passed += 1
            else:
                result['error'] = f"Expected: {expected_norm}, Got: {actual}"
                
        except NotImplementedError:
            result['error'] = "NotImplementedError - Function not implemented"
        except Exception as e:
            result['error'] = f"{type(e).__name__}: {str(e)}"
        
        results.append(result)
    
    return passed, results


def test_dpll(test_cases: List[Dict]) -> Tuple[int, List[Dict]]:
    """
    Test the dpll function with given test cases.
    Returns: (passed_count, results)
    """
    if not DPLL_IMPORT_SUCCESS:
        return 0, []
    
    passed = 0
    results = []
    
    for test_case in test_cases:
        result = {
            'id': test_case['id'],
            'description': test_case['description'],
            'passed': False,
            'error': None
        }
        
        try:
            # Convert clauses to sets
            clauses = [set(clause) for clause in test_case['clauses']]
            
            # Call dpll
            sat, assignment = dpll(clauses)
            
            # Check satisfiability
            if sat != test_case['expected_sat']:
                result['error'] = f"Expected SAT={test_case['expected_sat']}, Got SAT={sat}"
            elif sat and 'expected_assignment' in test_case:
                # Verify the assignment actually satisfies the formula
                if not verify_dpll_assignment(test_case['clauses'], assignment):
                    result['error'] = f"Assignment {assignment} does not satisfy the formula"
                else:
                    result['passed'] = True
                    passed += 1
            else:
                result['passed'] = True
                passed += 1
                
        except NotImplementedError:
            result['error'] = "NotImplementedError - Function not implemented"
        except Exception as e:
            result['error'] = f"{type(e).__name__}: {str(e)}"
            # Uncomment for debugging:
            # traceback.print_exc()
        
        results.append(result)
    
    return passed, results


def print_results(module_name: str, results: List[Dict], score: int, max_score: int):
    """Print test results for a module."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{module_name} Test Results{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
    
def print_results(module_name: str, results: List[Dict], passed: int, total: int):
    """Print test results for a module."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{module_name} Test Results{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    for result in results:
        status_icon = f"{Colors.GREEN}✓{Colors.END}" if result['passed'] else f"{Colors.RED}✗{Colors.END}"
        status_text = f"{Colors.GREEN}PASSED{Colors.END}" if result['passed'] else f"{Colors.RED}FAILED{Colors.END}"
        
        print(f"{status_icon} Test {result['id']}: {result['description']}")
        print(f"   Status: {status_text}")
        
        if result['error']:
            print(f"   {Colors.RED}Error: {result['error']}{Colors.END}")
        print()
    
    percentage = (passed / total * 100) if total > 0 else 0
    color = Colors.GREEN if percentage >= 70 else Colors.YELLOW if percentage >= 50 else Colors.RED
    
    print(f"{Colors.BOLD}Result: {color}{passed}/{total} tests passed ({percentage:.1f}%){Colors.END}\n")


def main():
    """Main autograder function."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Propositional Logic Autograder{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Testing: to_cnf.py and dpll.py{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")
    
    # Load test cases
    testcases_dir = os.path.join(os.path.dirname(__file__), 'testcases')
    
    try:
        with open(os.path.join(testcases_dir, 'cnf_test_cases.json'), 'r') as f:
            cnf_test_cases = json.load(f)['test_cases']
    except Exception as e:
        print(f"{Colors.RED}Error loading CNF test cases: {e}{Colors.END}")
        cnf_test_cases = []
    
    try:
        with open(os.path.join(testcases_dir, 'dpll_test_cases.json'), 'r') as f:
            dpll_test_cases = json.load(f)['test_cases']
    except Exception as e:
        print(f"{Colors.RED}Error loading DPLL test cases: {e}{Colors.END}")
        dpll_test_cases = []
    
    # Test to_cnf
    if CNF_IMPORT_SUCCESS:
        cnf_passed, cnf_results = test_to_cnf(cnf_test_cases)
        cnf_total = len(cnf_test_cases)
        print_results("to_cnf.py", cnf_results, cnf_passed, cnf_total)
    else:
        print(f"{Colors.RED}Skipping to_cnf tests due to import error{Colors.END}\n")
        cnf_passed, cnf_total = 0, len(cnf_test_cases)
    
    # Test dpll
    if DPLL_IMPORT_SUCCESS:
        dpll_passed, dpll_results = test_dpll(dpll_test_cases)
        dpll_total = len(dpll_test_cases)
        print_results("dpll.py", dpll_results, dpll_passed, dpll_total)
    else:
        print(f"{Colors.RED}Skipping DPLL tests due to import error{Colors.END}\n")
        dpll_passed, dpll_total = 0, len(dpll_test_cases)
    
    # Overall results
    total_passed = cnf_passed + dpll_passed
    total_tests = cnf_total + dpll_total
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}Overall Results{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")
    
    print(f"to_cnf.py:  {cnf_passed}/{cnf_total} tests passed")
    print(f"dpll.py:    {dpll_passed}/{dpll_total} tests passed")
    print(f"{Colors.BOLD}{'-'*70}{Colors.END}")
    
    color = Colors.GREEN if overall_percentage >= 70 else Colors.YELLOW if overall_percentage >= 50 else Colors.RED
    color = Colors.GREEN if overall_percentage >= 70 else Colors.YELLOW if overall_percentage >= 50 else Colors.RED
    print(f"{Colors.BOLD}Total: {color}{total_passed}/{total_tests} tests passed ({overall_percentage:.1f}%){Colors.END}\n")


if __name__ == "__main__":
    main()