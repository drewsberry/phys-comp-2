# Library imports
from __future__ import division # Division always returns float
import argparse

# Custom libraries
import laplace_solve as lps
import plotting
import matrix_io as mio

parser = argparse.ArgumentParser(description="Solving Laplace equation in two dimensions.")

parser.add_argument("method", choices = ["jacobi", "gauss-seidel"], help="""
                    iterative method to use. Both Jacobi and Gauss-Seidel methods are
                    supported.""")

parser.add_argument("-i","--input",
                    help="take boundary conditions from matrix input file")

parser.add_argument("-o","--output", 
                    help="write output solution matrix to file.")

parser.add_argument("-b","--boundary", 
                    choices = ["plane", "capacitor", "point_charge", "net", 
                               "cross"],
                    help="use in-built boundary conditions.")

parser.add_argument("-e", "--error", type=float, default=1e-4,
                    help="change the absolute error tolerance for convergence.")

parser.add_argument("-x", "--xnum", type=int, default=50, help="""
                    change the number of x nodes in the grid. Normal values are
                    between 25 and 100.""")

parser.add_argument("-y", "--ynum", type=int, default=50, help="""
                    change the number of y nodes in the grid. Normal values are
                    between 25 and 100""")

parser.add_argument("-p", "--plot", choices = ["surf", "contour", "vector"], nargs="*",
                    help="plot resulting solution to eps file.")

parser.add_argument("-w", "--printout", action="store_true",
                    help="print out resulting solution to stdout.")

args = parser.parse_args()

spacing = 1/128
matrix = None

if args.input:
    print "Taking input boundary conditions from file {0}... ".format(args.input),
    matrix, args.xnum, args.ynum = lpio.input_matrix(args.input)
    print "done"

print "Iteratively solving Laplace's equation using {0} method...\n".format(args.method.title())
solution = lps.solve_laplace(args.xnum, args.ynum, args.method, err_tol=args.error,
                             input_matrix=matrix, boundary_cond = args.boundary)
print "\n... done"

if args.plot:
    for i in range(len(args.plot)):
        if args.plot[i] == "surf":
            plotting.plot_surf(args.xnum, args.ynum, spacing, solution)
        if args.plot[i] == "contour":
            plotting.plot_contour(args.xnum, args.ynum, spacing, solution)
        if args.plot[i] == "vector":
            plotting.plot_vector(args.xnum, args.ynum, spacing, solution)

if args.output:
    print "\nPrinting solution to file... ",
    mio.print_matrix_to_file(solution, args.output)
    print "done"

if args.printout:
    print "\nPrinting solution to stdout... "
    mio.print_matrix(solution)
    print "... done"
