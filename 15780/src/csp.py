#! /usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
import sys

sys.setrecursionlimit(20000)

class CSP:

	def __init__(self, vars, domains, neighbors, token_arr):
		vars = vars or domains.keys()
		self.vars = vars; self.domains = domains; self.neighbors = neighbors
		self.token_arr = token_arr; self.curr_domains = None; self.is_assigned = False
		self.assigned_role = None; self.assigned_token_arr = []; self.nassigns = 0; self.node_expanded = 0
		self.conflict_set = []; self.deadend = None; self.prev_conflict_set = []
		for x in range(0,len(self.vars)):
			self.conflict_set.append([])

	def different_value_constraints(self, varA, valueA, varB, valueB):
		if self.is_assigned:
			# check whether varA and varB have tokens
			if varA in self.token_arr and varB in self.token_arr:
				return valueA == valueB and valueA == self.assigned_role
			elif varA in self.token_arr and not varB in self.token_arr:
				return valueA == self.assigned_role and valueA != valueB
			elif varB in self.token_arr and not varA in self.token_arr:
				return valueB == self.assigned_role and valueA != valueB
			else:
				return valueA != valueB
		else:
			if varA in self.token_arr and varB in self.token_arr:
				if valueA == valueB:
					self.assigned_role = valueA; self.is_assigned = True
					return True
				else:
					return False
			elif varA in self.token_arr and not varB in self.token_arr:
				if valueA != valueB:
					self.assigned_role = valueA; self.is_assigned = True
					return True
				else:
					return False
			elif varB in self.token_arr and not varA in self.token_arr:
				if valueA != valueB:
					self.assigned_role = valueB; self.is_assigned = True 
					return True
				else:
					return False	
			else:
				return valueA != valueB
	
	def assign(self, var, val, assignment):
		assignment[var] = val
		self.nassigns += 1
		if  var in self.token_arr and not var in self.assigned_token_arr:
			if not self.is_assigned:
				self.is_assigned = True
				self.assigned_role = val
			self.assigned_token_arr.append(var)

	def unassign(self, var, assignment):
		if var in assignment:
			del assignment[var]

	def check_token_assignment(self, var):
		if var in self.token_arr and var in self.assigned_token_arr:
			del self.assigned_token_arr[self.assigned_token_arr.index(var)]
		if self.assigned_token_arr == []:
			self.is_assigned = False; self.assigned_role = None
 

	def nconflicts(self, var, val, assignment):
		def conflict(var2):
			return (var2 in assignment and not self.different_value_constraints(var, val, var2, assignment[var2]))
		return count_if(conflict, self.neighbors[var])

	def goal_test(self, state):
		assignment = dict(state)
		return (len(assignment) == len(self.vars) and every(lambda var: self.nconflicts(var, assignment[var], assignment) == 0, self.vars))
		
	def initialize_curr_domains(self):
		if self.curr_domains is None:
			self.curr_domains = dict((v, list(self.domains[v])) for v in self.vars)

	def remove_other_values(self, var, value):
		self.initialize_curr_domains()
		removals = [(var, a) for a in self.curr_domains[var] if a != value]
		self.curr_domains[var] = [value]
		return removals

	def prune(self, var, value, removals):
		self.curr_domains[var].remove(value)
		if removals is not None: removals.append((var, value))

	def choices(self, var):
		return (self.curr_domains or self.domains)[var]

	def infer_assignment(self):
		self.initialize_curr_domains()
		return dict((v, self.curr_domains[v][0]) for v in self.vars if len(self.curr_domains[v] == 1))
		
	def restore(self, removals):
		for B, b in removals:
			self.curr_domains[B].append(b)
	
	def conflict_vars(self, current_assignment):
		return [var for var in self.vars if self.nconflicts(var, current_assignment[var], current_assignment) > 0]


# Variable ordering

def first_unassigned_variable(assignment, csp):
	return find_if(lambda var: var not in assignment, csp.vars)

def mrv(assignment, csp):
	return choose_mrv([v for v in csp.vars if v not in assignment],
							lambda var: num_legal_values(csp, var, assignment))

def num_legal_values(csp, var, assignment):
	if csp.curr_domains:
		return len(csp.curr_domains[var])
	else:
		return count_if(lambda val: csp.nconflicts(var, val, assignment) == 0, csp.domains[var])

# Value ordering

def unordered_domain_values(var, assignment, csp):
	return csp.choices(var)

def lcv(var, assignment, csp):
	return sorted(csp.choices(var), key = lambda val: csp.nconflicts(var, val, assignment))

# Inference

def no_inference(csp, var, value, assignment, removals):
	return True

def forward_checking(csp, var, value, assignment, removals):
	for B in csp.neighbors[var]:
		if B not in assignment:
			for b in csp.curr_domains[B][:]:
				if not csp.different_value_constraints(var, value, B, b):
					csp.prune(B, b, removals)
			if not csp.curr_domains[B]:
				return False
	return True

def mac(csp, var, value, assignment, removals):
	return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)
# --------------------------- Backtracking -----------------------------
def backtracking_search(csp, 
						select_unassigned_variable = first_unassigned_variable,
						order_domain_values = unordered_domain_values,
						inference = no_inference):

	def backtrack(assignment):
		if len(assignment) == len(csp.vars):
			return assignment
		var = select_unassigned_variable(assignment, csp)
		for value in order_domain_values(var, assignment, csp):
			if csp.nconflicts(var, value, assignment) == 0:
				csp.assign(var, value, assignment)
				csp.node_expanded += 1
				removals = csp.remove_other_values(var, value)
				if inference(csp, var, value, assignment, removals):
					result = backtrack(assignment)
					if result is not None:
						return result
				csp.restore(removals)
			csp.check_token_assignment(var)
		csp.unassign(var, assignment)
		return None

	result = backtrack({})
	assert result is None or csp.goal_test(result)
	return result

#--------------------------------- Back jumping ----------------------------------
def backjumping_search(csp,
				select_unassigned_variable = first_unassigned_variable,
				order_domain_values = unordered_domain_values,
				inference = no_inference, is_conflict_directed=False):

	
	def updateCF(var, csp):
		for x in csp.vars:
			if var in csp.neighbors[x] and var not in csp.conflict_set[x]:
				csp.conflict_set[x].append(var)
		return csp.conflict_set

	def updateCF_backjumping(var, csp, assigned_var, is_conflict_directed):
		tmp_conflict_set = []
		for x in csp.vars:
			cf_tmp = []
			if is_conflict_directed:
				if x == var:
					set_tmp = csp.conflict_set[x] + csp.prev_conflict_set
					csp.conflict_set[x] = set_tmp
			for y in range(0, len(assigned_var)-1):
				if assigned_var[y] in csp.conflict_set[x]:
					cf_tmp.append(assigned_var[y])
			csp.conflict_set[x] = cf_tmp
		return csp.conflict_set

	assigned_var = []	
	def backjumping(assignment):
		if len(assignment) == len(csp.vars):
			return assignment
		var = select_unassigned_variable(assignment, csp)
		for value in order_domain_values(var, assignment, csp):
			if csp.nconflicts(var, value, assignment) == 0:
				csp.assign(var, value, assignment)
				csp.node_expanded += 1
				assigned_var.append(var)
				csp.conflict_set = updateCF(var, csp)
				removals = csp.remove_other_values(var, value)
				if inference(csp, var, value, assignment, removals):
					result = backjumping(assignment)
					if result is not None:
						return result
				csp.restore(removals)
			if csp.deadend != None and var in csp.conflict_set[csp.deadend]:
				csp.deadend = None
				csp.conflict_set = updateCF_backjumping(var, csp, assigned_var, is_conflict_directed)
			csp.unassign(var, assignment)
			if var in assigned_var:
				del assigned_var[assigned_var.index(var)]
			if csp.deadend != None:
				return None
		csp.deadend = var; 
		csp.prev_conflict_set = csp.conflict_set[csp.deadend]
		return None

	result = backjumping({})
	assert result is None or csp.goal_test(result)
	return result

# ----------------------------------- AC-3 ------------------------------------------------
def AC3(csp, queue = None, removals = None):

	if queue is None:
		queue = [(Xi, Xk) for Xi in csp.vars for Xk in csp.neiborghs[Xi]]
	csp.initialize_curr_domains()
	while queue:
		(Xi, Xk) = queue.pop()
		if revise(csp, Xi, Xk, removals):
			if not csp.curr_domains[Xi]:
				return False
			for Xk in csp.neighbors[Xi]:
				if Xk != Xi:
					queue.append((Xk, Xi))
	return True

def revise(csp, Xi, Xk, removals):

	revise = False
	for x in csp.curr_domains[Xi][:]:
		if every(lambda y: not csp.different_value_constraints(Xi, x, Xk, y), csp.curr_domains[Xk]):
			csp.prune(Xi, x, removals)
			return True
	return revise
