#!/usr/bin/python -O

import sys
import random
import csv
import hashlib

# 
# John P. Dickerson -- 24 January 2013 -- WarOfDoom Graph Generator
# Homework #1: Knowledge Representation, SAT, and CSPs
# Graduate AI 2013 -- Professors Tuomas Sandholm and Manuela Veloso
#
# Erdos-Renyi graph generator for Problem #3.
#
# Sample usage:
#   $> python generator.py 10 0.1 3 sample.graph [jpdicker]
#   This generates a 10-vertex graph, 10% probability of edge between vertices,
#   adds 3 tokens, and outputs the graph in HW #1 format to file "sample.graph"
#   If the optional seed argument is provided, we seed(sha hash of arg)
#


def generate(n, p, k, outfile):


    # Naive |V|^2 Erdos-Renyi graph generator
    print 'Generating G(%d,%f) with %d tokens.' % (n, p, k)
    
    E = []
    edge_ct = 0
    for src in range(n-1):
        edges = []
        for dst in range(src+1,n):
            if src != dst and random.random() < p:
                edges.append(dst)
                edge_ct += 1
        E.append(edges)
                
    # Choose k unique vertices to have tokens
    token_verts = random.sample(range(n), k)



    print "Writing to %s" % (outfile)
    with open(outfile, "wb") as f:
        writer = csv.writer(f, delimiter=' ')

        # Write the graph details
        writer.writerow([n, edge_ct, k])

        # Write the adjecency list
        for src, src_edges in enumerate(E):
            for dst in src_edges:
                writer.writerow([src, dst])

        # Write which vertices are token vertices
        for v in token_verts:
            writer.writerow([v])

        f.close()


if __name__ == '__main__':

    if(len(sys.argv) < 5 or len(sys.argv) > 6):
        print "Usage: python generator.py <num-vertices> <prob-of-edge> <num-tokens> <output-file> [<seed>]"
        sys.exit(-1)

    # Four parameters: num vertices, prob of edges, num tokens, output file
    n = int(sys.argv[1])
    p = float(sys.argv[2])
    k = int(sys.argv[3])
    outfile = sys.argv[4]

    if len(sys.argv) == 6:
        # If the user passes in a seed, seed our random roller with this; otherwise,
        # seed the way Python normally does (I guess using systime)
        seed_str = sys.argv[5]
        seed = int(hashlib.md5(seed_str).hexdigest(), 16)
        random.seed(seed)
    

    # Make sure user-supplied parameters are shipshape 
    assert n > 0, 'Number of vertices must be a positive integer'
    assert p >= 0.0 and p <= 1.0, 'Probability of edges must be a real number in [0,1]'
    assert k >= 0 and k <= n, 'Number of tokens must be a nonnegative integer and less than |V|'
    
    

    # Generate the graph
    generate(n,p,k,outfile)

    print "Done"
    
