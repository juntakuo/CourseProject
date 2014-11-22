#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, getopt
import fileinput
import time
from utils import *
from csp import *
sys.setrecursionlimit(20000)

argv = sys.argv[1:]
inputfile = ''
method = ''
try:
	opts, args = getopt.getopt(argv, "hi:m:", ["ifile=", "method="])
except getopt.GetoptError:
	print '[Usage]: python main.py -i <inputfile> -m <method>'
	sys.exit(2)
for opt, arg in opts:
	if opt == '-h':
		print '[Usage]: python main.py -i <inputfile> -m <method>'
		print 'Methods:\n	default : backtracking + MRV + LCV + AC3'
		print '	method: 1 = backtracking'
		print '	method: 2 = backtracking + MRV'
		print '	method: 3 = backtracking + LCV'
		print '	method: 4 = backtracking + MRV + LCV'
		print '	method: 5 = backtracking + MRV + LCV + FC'
		print '	method: 6 = backjumping + MRV + LCV'
		print '	method: 7 = backjumping + MRV + LCV + FC'
		print '	method: 8 = conflict-directed backjumping + MRV + LCV + FC'
		sys.exit()
	elif opt in ("-i", "--ifile"):
		inputfile = arg
	elif opt in ("-m", "--method"):
		method = arg

#read in file
try:
	ifs = open(inputfile, 'rb') 
except IOError as e:
	print 'The file \"',inputfile, '\" does not exist!!.\n[Usage]: ./test.py -i <inputfile> -m <method>'
	sys.exit(2)


# construct CSP 

first_line = ifs.readline().rstrip('\r\n').split(' ')
num_of_nodes = int(first_line[0])
num_of_edges = int(first_line[1])
num_of_tokens = int(first_line[2])

# construct nodes
neighbors = DefaultDict([]);
for i in xrange(num_of_nodes):
	neighbors.setdefault(i, [])
# link edges
for idx in xrange(num_of_edges):
	line = ifs.readline().rstrip('\r\n').split(' ')
	neighbors[int(line[0])].append(int(line[1]))
	neighbors[int(line[1])].append(int(line[0]))
	# label toke
token_arr = []
for idx in xrange(num_of_tokens):
	line = ifs.readline().rstrip('\r\n').split(' ')
	token_arr.append(int(line[0]))

for idx1 in token_arr:
	for idx2 in token_arr:
		if not idx2 in neighbors[idx1] and idx1 != idx2:
			neighbors[idx1].append(idx2)
			neighbors[idx1].sort()

problem = CSP(neighbors.keys(), UniversalDict(['Blacksmith', 'Archer', 'Sorceress', 'Warrior']), neighbors, token_arr)

# decide which method should be used
start = time.clock()
if method == '1':
	assignment = backtracking_search(problem)
elif method == '2':
	assignment = backtracking_search(problem, select_unassigned_variable = mrv, order_domain_values = unordered_domain_values, inference = no_inference)
elif method == '3':
	assignment = backtracking_search(problem, select_unassigned_variable =  first_unassigned_variable, order_domain_values = lcv, inference = no_inference)
elif method == '4':
	assignment = backtracking_search(problem, select_unassigned_variable = mrv, order_domain_values = lcv, inference = no_inference)
elif method == '5':
	assignment = backtracking_search(problem, select_unassigned_variable = mrv, order_domain_values = lcv, inference = forward_checking)
elif method == '6':
	assignment = backjumping_search(problem, select_unassigned_variable = mrv, order_domain_values = lcv, inference = no_inference)
elif method == '7':
	assignment = backjumping_search(problem, select_unassigned_variable = mrv, order_domain_values = lcv, inference = forward_checking)
elif method == '8':
	assignment = backjumping_search(problem, select_unassigned_variable = mrv, order_domain_values = lcv, inference = forward_checking, is_conflict_directed = True)
else:
	assignment = backtracking_search(problem, select_unassigned_variable = mrv, order_domain_values = lcv, inference = mac)

end = time.clock()

if assignment == None: result = 'FALSE'
else: result = 'TRUE'

print 'tkuo ', inputfile, problem.node_expanded, (end-start), result


