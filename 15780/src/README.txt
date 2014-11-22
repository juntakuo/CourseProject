How to run the code:

please type this command on the command line:

python main.py -i <inputfile name> -m <method>

The number of each method is shown below:

method: 1 : backtracking
method: 2 : backtracking + MRV
method: 3 : backtracking + LCV
method: 4 : backtracking + MRV + LCV
method: 5 : backtracking + MRV + LCV + FC
method: 6 : backjumping + MRV + LCV
method: 7 : backjumping + MRV + LCV + FC
method: 8 : conflict-directed backjumping + MRV + LCV + FC
other arbitrary number : The improved solver, performing backtracking + MRV + LCV + AC3

For example, if we want to search the solution of a graph named 'easy_planar_100_0.graph' with 'Basic backtracking', the command should be:

python main.py -i easy_planar_100_0.graph -m 1

If we want to use the 'improved solver', type any number after the parameter '-m', for example

python main.py -i easy_planar_100_0.graph -m 21
