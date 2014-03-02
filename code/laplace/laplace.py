# Library imports
from __future__ import division # Division always returns float
import argparse

# Custom libraries
import laplace_solve as lps
import laplace_plot as lpp

parser = argparse.ArgumentParser(description='Solving Laplace equation in two dimensions.')

parser.add_argument('-i','--input', action='store_true',
					help='take boundary conditions from matrix input file')

parser.add_argument('-o','--output', 
					help='write output solution matrix to file.')

parser.add_argument('-b','--boundary', 
					choices = ["plane", "capacitor", "point_charge", "net", 
							   "cross"],
					help='use in-built boundary conditions.')

parser.add_argument('-e', '--error', type=int, default=1e-2,
					help='change the absolute error tolerance for convergence.')

parser.add_argument('-x', '--xnum', type=int, default=50,
					help='change the number of x nodes in the grid.')

parser.add_argument('-y', '--ynum', type=int, default=50,
					help='change the number of y nodes in the grid.')

parser.add_argument('-p', '--plot', action="store_true",
					help='plot resulting solution to eps file.')

parser.add_argument('-w', '--printout', action='store_true',
					help='print out resulting solution to stdout.')

args = parser.parse_args()

spacing = 1/128
matrix = None

if args.input:
	print "Taking input boundary conditions from file {0}".format(args.input),
	matrix, args.xnum, args.ynum = lps.input_matrix("input_matrix.dat")
	print "done"

print "Iteratively solving Laplace's equation... "
solution = lps.solve(args.xnum, args.ynum, err_tol=args.error, 
					 input_matrix=matrix, boundary_cond = args.boundary)
print "... done"

if args.plot:
	print "Printing solution to encapsulated postscript... ",
	lpp.plot(args.xnum, args.ynum, spacing, solution)
	print "done"

if args.output:
	print "Printing solution to file... ",
	lps.print_matrix_to_file(solution, args.output)
	print "done"

if args.printout:
	print "Printing solution to stdout... "
	lps.print_matrix(solution)
	print "... done"