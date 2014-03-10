# Library imports
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt

    from matplotlib import cm
    from matplotlib import rc
    from mpl_toolkits.mplot3d import Axes3D
except ImportError as e:
    print "Error importing matplotlib library. You will not be able to use the "\
          "'-p' or '--plot' option."
    print "Error message: {}\n".format(e)
# This is so the program will still run without having the matplotlib plotting
# libraries installed, just without the ability to plot.

import matrix_io as mio

rc("text", usetex=True)

def plot_surface(num_x, num_y, spacing, grid, title="varphi", filename="surface"):
    # Use matplotlib.pyplot to plot surface of potential field.

    x = np.linspace(0, num_x*spacing, num_x)
    y = np.linspace(0, num_y*spacing, num_y)  
    X, Y = np.meshgrid(x,y)

    fig = plt.figure()

    print "\nPlotting solution to surface plot... ",
    surf_axes = fig.gca(projection='3d')
    surf_plot = surf_axes.plot_surface(X, Y, grid.transpose(), rstride=1, cstride=1,
        cmap=cm.hot, linewidth=0, antialiased=True)
    surf_plot = surf_axes.plot_surface(X, Y, grid.transpose(), rstride=1, cstride=1,
        cmap=cm.hot, linewidth=0, antialiased=True)
    # Plotting twice eradicates white line artefacts
    print "done"

    surf_axes.set_xlabel("$x$")
    surf_axes.set_ylabel("$y$")
    if title == "varphi":
        surf_axes.set_title("$\\varphi(x,y)$")
    else:
        surf_axes.set_title("$\\"+title+"(x,y)$")
    # Allows for subtly different title for Laplace equation and heat diffusion.

    full_fname = "plots/" + filename + ".eps"
    print "Saving surf plot to file '{}'... ".format(full_fname),
    plt.savefig(full_fname, bbox_inches="tight")
    print "done"

def plot_contour(num_x, num_y, spacing, grid, title="varphi", filename="contour"):
    # Use matplotlib to plot contours of potential field.

    x = np.linspace(0, num_x*spacing, num_x)
    y = np.linspace(0, num_y*spacing, num_y)  
    X, Y = np.meshgrid(x,y)

    if title == "phi":
        fig = plt.figure(figsize=(num_x/5,num_y/5))
    else:
        fig = plt.figure()

    print "\nPlotting solution to contour plot... ",
    cont_plot = plt.contourf(X, Y, grid.transpose(), 100, rstride=1, cstride=1,
                             cmap=cm.hot, linewidth=0)
    cont_plot = plt.contourf(X, Y, grid.transpose(), 100, rstride=1, cstride=1,
                             cmap=cm.hot, linewidth=0)
    # Plotting twice eradicates white line artefacts
    cbar = plt.colorbar()
    cbar.solids.set_edgecolor("face")
    plt.draw()
    # Eradicates white line artefacts in colorbar
    print "done"

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    if title == "varphi":
        plt.title("$\\varphi(x,y)$")
    else:
        plt.title("$\\"+title+"(x,y)$")
    # I want a subtly different title for Laplace equation and heat diffusion

    full_fname = "plots/" + filename + ".eps"
    print "Saving contour plot to file '{}'... ".format(full_fname),
    plt.savefig(full_fname, bbox_inches="tight")
    print "done"

def plot_vector(num_x, num_y, spacing, grid, title="varphi", filename="vector"):
    # Plot the vector gradient of potential field using arrows.

    Y, X = np.mgrid[0:num_x*spacing:complex(0,num_x),
                    0:num_y*spacing:complex(0,num_y)]

    print "\nFinding gradient of solution... ",
    vector_u, vector_v = np.gradient(grid.transpose())
    print "done"

    vector_u = np.zeros((num_x, num_y)) - vector_u
    vector_v = np.zeros((num_x, num_y)) - vector_v

    magnitude = np.sqrt(vector_u*vector_u + vector_v*vector_v)

    fig = plt.figure()

    lw = 5*magnitude/magnitude.max()

    print "Plotting gradient of solution to vector plot... ",
    stream_plot = plt.streamplot(X, Y, vector_v, vector_u, color=magnitude, 
                                 linewidth=lw, cmap=cm.hot)
    cbar = plt.colorbar()
    cbar.solids.set_edgecolor("face")
    plt.draw()
    print "done"

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$\mathbf{E}(x,y)$")

    full_fname = "plots/" + filename + ".eps"
    print "Saving vector plot to file '{}'... ".format(full_fname),
    plt.savefig(full_fname, bbox_inches="tight")
    print "done"

def plot_magnitude(num_x, num_y, spacing, grid, filename="magnitude"):
    # Plot the magnitude of the electric field as a contour map

    Y, X = np.mgrid[0:num_x*spacing:complex(0,num_x),
                    0:num_y*spacing:complex(0,num_y)]

    print "\nFinding magnitude of gradient of solution... ",
    vector_u, vector_v = np.gradient(grid.transpose())

    vector_u = np.zeros((num_x, num_y)) - vector_u
    vector_v = np.zeros((num_x, num_y)) - vector_v

    magnitude = np.sqrt(vector_u*vector_u + vector_v*vector_v)
    print "done"

    print "Plotting magnitude of gradient of solution to contour plot... ",
    fig = plt.figure()

    cont_plot = plt.contourf(X, Y, magnitude, 100, rstride=1, cstride=1,
                             cmap=cm.hot, linewidth=0)
    cont_plot = plt.contourf(X, Y, magnitude, 100, rstride=1, cstride=1,
                             cmap=cm.hot, linewidth=0)
    cbar = plt.colorbar()
    cbar.solids.set_edgecolor("face")
    plt.draw()

    print "done"

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$|\mathbf{E}(x,y)|$")

    full_fname = "plots/" + filename + ".eps"
    print "Saving vector plot to file '{}'... ".format(full_fname),
    plt.savefig(full_fname, bbox_inches="tight")
    print "done"

def plot_normal(num_x, solution, filename="normal"):
    # Normal 1d plot

    x = np.linspace(0, num_x, num_x)

    fig = plt.figure()

    print "\nPlotting to normal 1D plot...",
    plt.plot(x, solution[0,:])
    print "done"

    plt.xlabel("$x$ /cm")
    plt.ylabel("Temperature, $\phi$ /K")
    plt.title("$\phi(x)$")

    full_fname = "plots/" + filename + ".eps"
    print "Saving normal plot to file '{}'...".format(full_fname),
    plt.savefig(full_fname, bbox_inches="tight")
    print "done"