#!/usr/bin/python -O

import sys
import random
import csv
import hashlib

import matplotlib.delaunay as tri
import pylab
import numpy

# 
# John P. Dickerson -- 27 January 2013 -- WarOfDoom Graph Generator
# Homework #1: Knowledge Representation, SAT, and CSPs
# Graduate AI 2013 -- Professors Tuomas Sandholm and Manuela Veloso
#
# Planar graph generator for Problem #3
#
# Sample usage:
#   $> python generator.py 10 3 sample.graph [jpdicker]
#   This generates a 10-vertex graph, random R^2 with Delaunay triangulation,
#   adds 3 tokens, and outputs the graph in HW #1 format to file "sample.graph"
#   If the optional seed argument is provided, we seed(sha hash of arg)
#


def generate(n, k, outfile):


    # Delaunay triangulation of random points in R^2
    print 'Generating %d-planar graph with %d tokens.' % (n, k)

    x,y = numpy.array(numpy.random.standard_normal((2,n)))
    c,E,tris,ngbr = tri.delaunay(x,y)
                
    # Choose k unique vertices to have tokens
    token_verts = random.sample(range(n), k)

    print "Writing to %s" % (outfile)
    with open(outfile, "wb") as f:
        writer = csv.writer(f, delimiter=' ')

        # Write the graph details
        writer.writerow([n, len(E), k])

        # Write the adjecency list
        for edge in E:
            writer.writerow(edge)

        # Write which vertices are token vertices
        for v in token_verts:
            writer.writerow([v])  

        f.close()


if __name__ == '__main__':

    if(len(sys.argv) < 4 or len(sys.argv) > 5):
        print "Usage: python generator_planar.py <num-vertices> <num-tokens> <output-file> [<seed>]"
        sys.exit(-1)

    # Four parameters: num vertices, prob of edges, num tokens, output file
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    outfile = sys.argv[3]

    if len(sys.argv) == 5:
        # If the user passes in a seed, seed our random roller with this; otherwise,
        # seed the way Python normally does (I guess using systime)
        seed_str = sys.argv[4]
        seed = int(hashlib.md5(seed_str).hexdigest(), 16)
        random.seed(seed)
    

    # Make sure user-supplied parameters are shipshape 
    assert n > 0, 'Number of vertices must be a positive integer'    
    assert k >= 0 and k <= n, 'Number of tokens must be a nonnegative integer and less than |V|'
    
    

    # Generate the graph
    generate(n,k,outfile)

    print "Done"
    
