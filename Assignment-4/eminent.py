###########################################################################
###########                                                     ###########
###########                 AI Assignment-4                     ###########
###########                 Satvik Golechha                     ###########
###########                 2017A7PS0117P                       ###########
###########                                                     ###########
###########################################################################


# import inbuilt python libraries
from typing import Generic, TypeVar, List, Dict, Optional, Tuple
from abc import ABC, abstractmethod
from copy import copy, deepcopy
from itertools import combinations
import math
import random
import queue


V = TypeVar('V')        #   variable type
D = TypeVar('D')        #   domain type


class constraint(Generic[V, D], ABC):
    '''
        - base class for all constraints
        - initializer sets the variables that the constraint is between
        - satisfied is an abstract method that must be overridden by problem-specific subclasses
    '''

    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


class constraint_satisfaction_problem(Generic[V, D]):
    '''
        - base class for all CSPs
        - a constraint satisfaction problem consists of variables of type V
        - that have ranges of values known as domains of type D and constraints
        - that determine whether a particular variable's domain selection is valid
        - INIT: sets up the variables and domains, with no constraints
        - add_constraint() can be used to add any number of constraints
    '''

    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[constraint[V, D]]] = {}

        # no constraints on each variable
        for v in self.variables:
            self.constraints[v] = []
            # every variable must have a domain, otherwise it's an error
            if v not in domains:
                raise LookupError(f"Variable {v} has no domain")

    
    def add_constraint(self, constraint: constraint[V, D]) -> None:
        '''
            - for each variable participating in a constraint,
            - add to the list of constraints of that variable, 
            - this constraint
        '''
        for v in constraint.variables:
            # variable from constraint must exist in the problem
            if v not in self.variables:
                raise LookupError(f"Variable {v} does not exi..")
            else:
                self.constraints[v].append(constraint)

    
    def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
        '''
            - checks if a partial assignment is consistent wrt one variable
            - checks every constraint of that variable, and if any of them fails,
            - return False
        '''

        for c in self.constraints[variable]:
            if not c.satisfied(assignment):
                return False
        return True


    def backtracking_dfs_constraint_propagation(self, heur1, heur2, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        '''
            - DFS backtracking, while using constraint propagation
            - will use the implementation of backtracking_dfs
            - after trimming the domains using the 
            - AC-3 algorithm for Arc Consistency as shown in the textbook
        '''

        if self.arc_consistent():
            # solution exists
            return self.backtracking_dfs(heur1, heur2)
        else:
            # inconsistency
            return None

        
    def arc_consistent(self) -> bool:
        '''
            - AC-3 Algorithm
            - hard assumption is that all constraints
            - have been converted to binary constraints
            - before applying this function
        '''

        l: List[Generic[V, D]] = []

        for var in self.variables:
            for const in self.constraints[var]:
                if [const.variables[0], const.variables[1]] not in l and const.variables.__len__() == 2:
                    # binary constraints only
                    l.append([const.variables[0], const.variables[1]])

        while l.__len__() != 0:
            arc = l.pop()

            if self.revise(arc):
                # if we revise the domain of the first variable of the arc constraint
                if self.domains[arc[0]].__len__() == 0:
                    # not consistent
                    return False

                # else, add neighbors of that variable to the list
                for n in self.neighbors_not(arc[0], arc[1]):
                    l.append([n, arc[0]])
        
        return True


    def revise(self, arc):
        revised = False
        for x in self.domains[arc[0]]:
            no_val_satisfies = True
            for y in self.domains[arc[1]]:
                if eminent_personality_constraint([arc[0], arc[1]]).satisfied():
                    no_val_satisfies = False
            if no_val_satisfies:
                self.domains[arc[0]].remove(x)
                revised = True
            
        return revised


    def neighbors_not(self, var1, var2):
        # returns a list of neighbors of var1 which are not var2
        allcons = self.constraints[var1]

        n = []

        for c in allcons:
            v1 = c.variables[0] 
            v2 = c.variables[1]
            if v1 != var2 and v1 not in n:
                n.append(v1)
            if v2 != var2 and v2 not in n:
                n.append(v2)

        return n


    def backtracking_dfs(self, heur1, heur2, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
        '''
            - backtracking search for the CSP
            - includes use of heuristics to search for an assignment
            - which satisfies the problem's constraints
            - if no such assignment is found, returns None, 
            - else returns a solution assignment
        '''

        if assignment.__len__() == self.variables.__len__():
            # the partial assignment is complete, return the solution
            return assignment

        # get all the variables in the problem, but not in the assignment
        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        # to be replaced by select_unassigned_variable(CSP) if heur1 == 1, else taking the first unassigned
        var_un: V = self.select_unassigned_variable_degree(unassigned) if heur1 == 1 else unassigned[0]

        # again, to be replaced by order_domain_values(V, assn, CSP)
        dom_order = self.order_domain_values(var_un, assignment) if heur2 == 1 else self.domains[var_un]

        for v in dom_order:
            local_assignment = assignment.copy()
            local_assignment[var_un] = v

            # if the new assignment is consistent, we continue with the search, else we backtrack
            if self.consistent(var_un, local_assignment):
                result: Optional[V, D] = self.backtracking_dfs(heur1, heur2, local_assignment)
                # if result is not found, backtrack
                if result is not None:
                    return result
            
        return None

    
    def select_unassigned_variable_MRV(self, unassigned: List[V]) -> Optional[V]:
        '''
            - selects the best unassigned variable
            - from the list of unassigned, using the 
            - MRV (minimum remaining value) heuristic
            - returns None if list is empty
                - EDIT: This situation should never arise
                - unless the user changes these class functions
        '''
        
        min_options = math.inf
        for variable in unassigned:
            if self.domains[variable].__len__() < min_options:
                min_options = self.domains[variable].__len__()
                best_var = variable

        return best_var

    
    def select_unassigned_variable_degree(self, unassigned: List[V]) -> Optional[V]:
        '''
            - selects the best unassigned variable
            - from the list of unassigned, using the 
            - degree heuristic
            - returns None if list is empty
                - EDIT: This situation should never arise
                - unless the user changes these class functions
        '''
        
        max_constraints = - math.inf
        for variable in unassigned:
            if self.constraints[variable].__len__() > max_constraints:
                max_constraints = self.constraints[variable].__len__()
                best_var = variable

        return best_var

    
    def order_domain_values(self, variable: V, assignment: Dict[V, D]) -> List[D]:
        '''
            - selects the best domain order for given variable
            - from the list of options 
            -  currently, the heuristic used is the length of the domain value
            - since the heuristic is expected to depend on the problem at hand,
            - this method should be changed if it is required to use any particular heuristic like
            - least_constraining_value, etc
        '''
        
        return sorted(self.domains[variable], key = lambda x: str(x).__len__())
        


#######################################  
# this finishes the common part, now is the problem specefic implementation

def matrixify(groups: List[List[str]]) -> List[Tuple[str,str]]:
    '''
        - input: groups, as defined below
        - output: a list which, if has the tuple (a,b),
        - means that 'a' and 'b' have a group in common,
        - and hence, it's not wise to give them the same time slot
        - EDIT:
            - This method is not used in this implementation, but it is useful
            - to create the constraint_graph for the problem,
            - as is required in the problem as an image
    '''
    constraint_graph: List[Tuple[str,str]] = []

    for group in groups:
        for pair in list(combinations(group, 2)):
            if pair not in constraint_graph:
                constraint_graph.append(pair)
    
    return constraint_graph
                
           
class eminent_personality_constraint(constraint[str, int]):
    '''
        - defining a binary constraint for this problem
    '''
    def __init__(self, persons: List[str]) -> None:
        super().__init__(persons)
        self.one: str = persons[0]
        self.two: str = persons[1]

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        '''#
            - given a partial assignment, tells if it is satisfied or not
            - if for any a,b:
            - there's a group of students who wish to meet Na and Nb,
            - and if Na and Nb are assigned the same time slot,
            - then return false
            - in all other cases, the assignment is satisfying the constraint
            - EDIT:
                - this docstring is wrong, this is not how this works
        '''

        if self.one not in assignment or self.two not in assignment:
            # if they are not present, no chance not satisfying 
            return True

        else:
            if assignment[self.one] == assignment[self.two]:
                # doesn't satisfy all_diff for these two variables in the constraint_graph
                return False
            else:
                return True


if __name__ == "__main__":
    num_per: int = int(input("Enter the number of eminent persons: "))
    eminent_persons: List[str] = [''.join(['N',str(i+1)]) for i in range(num_per)]
    availability: Dict[str, List[int]] = {}
    
    # input the availability for all eminent personalities:
    print("In order to enter the free hours of all personalities, please enter them separated by commas.")
    print("For example, if N1 is free during 2nd, 5th and 7th hours, please enter: N2, N5, N7")

    for c in range(num_per):
        inp: str = input(f"Please enter free hours of N{str(c+1)}:")
        hours: List[int] = [int(h) for h in inp.split(sep=',')]
        availability[f'N{str(c+1)}']: List[int] = hours
    
    # input the availability for all eminent personalities:
    group_num: int = int(input("Enter the number of groups of students: "))
    
    groups: List[List[str]] = []
    
    print("In order to enter the persons each group wants to meet, please enter them separated by commas.")
    print("For example, if G1 wants to meet N2, N5 and N7 hours, please enter: N2, N5, N7")

    for g in range(group_num):
        inp: str = input(f"Please enter personalities wished by Group-{str(g+1)}:")
        pers: List[str] = [inp.split(sep=',')]
        groups.append(pers)

    print()

    search: int = int(input("Please enter 1 for dfs_bt and 0 for dfs_bt_constraint_prop: "))
    heur1: int = int(input("Please enter 1 for using MRV and 0 for not using: "))
    heur2: int = int(input("Please enter 1 for using degree heuristic and 0 for not using: "))

    print()
    # creating the problem instance
    scheduling: constraint_satisfaction_problem[str, int] = constraint_satisfaction_problem(eminent_persons, availability)
    
    for group in groups:
        for edge in list(combinations(group, 2)):
            scheduling.add_constraint(eminent_personality_constraint(edge))
    
    if search == 1:
        solution: Optional[Dict[int, int]] = scheduling.backtracking_dfs(heur1, heur2)

    if search == 0:
        solution: Optional[Dict[int, int]] = scheduling.backtracking_dfs_constraint_propagation(heur1, heur2)
    
    if solution is None:
        print("No solution found!")
    else:
        for k in solution.keys():
            print(f"{k}: {solution[k]}")

