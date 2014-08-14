Computational Physics: Exercise 2
---------------------------------

# Overview

This contains the files for the code and report of Exercise 2 of Computational Physics 301, entitled "Partial Differential Equations". The exercise contains three parts:

- Solving Laplace's equation in two dimensions;
- Solving the electric potential of a finite capacitor, investigating in particular the limit of an infinite place capacitor;
- Solving the heat diffusion equation for a hot metal rod.

This branch contains the actual Python code used to produce the program.

# Files

| Filename | Description |
| -------- | ----------- |
| laplace.py | General laplace solver. You can input your own matrices as boundary conditions with the '--input' or '-i' flags. More information, along with examples, is given in the 'example\_input' folder. The resulting potential field solution can be printed to standard output with '--printout' or '-w' options, or printed to file with '--output' or '-o'. The graphs can be plotted to potential surface, potential; contour, electric field vector field lines or electric field strength contour plots with the '--plot' or '-p' options. Note that either the Jacobi or Gauss-Seidel method must be chosen. In addition to taking boundary conditions from input file, there are also a number of in-built boundary conditions accessible with the '--boundary' or '-b' flags. The absolute error tolerance can be altered with the '--error' or '-e' flags, whilst the grid density can be changed with the '--xnum' or '-x' and '--ynum' or '-y' flags. Note that below ~20x20 the grid is too sparse to provide useful information, and above ~100x100 the convergence time goes into the tens of minutes (this is explained and analysed in the main body of the report).|
| laplace\_solve.py | This library file is the library that contains the functions used in laplace.py to solve the Laplace equation. Note that it is the laplace.py file that should be run to produce the results.|
| matrix\_io.py | This library file contains the input/output operations for matrix manipulation. It contains the methods for taking a matrix from a file and turning it into a NumPy array, printing matrices neatly to stdout and printing matrices to a separate file. This is used for both the Laplace and heat diffusion programs.|
| plotting.py | This library file contains the functions for plotting the graphs using matplotlib. This is not a necessary part of either of the programs, and the programs should work perfectly well without the matplotlib libraries installed on your system, although the programs display a message stating that you won't be able to use the plotting functions of the program. This is shared by both laplace.py and diffusion.py.|
| diffusion.py | Specific heat diffusion solver. This program solves the heat diffusion equation for an iron rod with one end in a hot furnace and with the other end either at room temperature or in ice. As with laplace.py, grid density, width and absolute eror tolerance can be changed with the '--xnum'/'-x', '--width'/'-w' and '--error'/'-e' flags, respectively. In addition, the '--cold' or '-c' flag determines whether one end of the rod is put in freezing ice. (Default is false.) There are equivalent print to stdout, print to file and plot to file options. Both the time step and the total time to simulate can be altered with the '--timestep'/'-s' and '--time'/'-t' flags, respectively. The '--time' option is ignored if the '--equilibrium'/'-q' flag is set to true, in which case the program continues until it reaches an equilibrium as defined by the absolute error tolerance (default is 1e-5).|
| diffusion\_evolve.py | This library file contains the functions needed for the diffusion.py program to solve the diffusion equation for the iron rod.|
| plots/ | The directory where plots are saved to.|
| animations/ | The directory containing animations demonstrating the limit taking process as the capacitor looks more and more likes an infinite plate capacitor. The surface plot animation in particular gives a visual insight into how the potential field approaches that of an infinite parallel plate capacitor.|
