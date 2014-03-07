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
    print "Error message: {}".format(e)

rc("text", usetex=True)

def plot_surf(num_x, num_y, spacing, grid, filename="surf"):
    # Use matplotlib.pyplot to create 3D surf plot of potential field.

    x = np.linspace(0, num_x*spacing, num_x)
    y = np.linspace(0, num_y*spacing, num_y)  
    X, Y = np.meshgrid(x,y)

    fig = plt.figure()

    print "\nPlotting solution to surf plot... ",
    surf_axes = fig.gca(projection='3d')
    surf_plot = surf_axes.plot_surface(X, Y, grid.transpose(), rstride=1, cstride=1,
        cmap=cm.hot, linewidth=0, antialiased=True)
    print "done"

    surf_axes.set_xlabel("$x$")
    surf_axes.set_ylabel("$y$")
    surf_axes.set_title("$\\varphi(x,y)$")

    full_fname = "plots/" + filename
    print "Saving surf plot to file '{}'... ".format(full_fname),
    plt.savefig(full_fname)
    print "done"

def plot_contour(num_x, num_y, spacing, grid, filename="contour.eps"):
    # Use matplotlib to plot contours of potential field.

    x = np.linspace(0, num_x*spacing, num_x)
    y = np.linspace(0, num_y*spacing, num_y)  
    X, Y = np.meshgrid(x,y)

    # fig = plt.figure()
    fig = plt.figure(figsize=(5,52))

    print "\nPlotting solution to contour plot... ",
    cont_plot = plt.contourf(X, Y, grid.transpose(), 100, rstride=1, cstride=1, 
        cmap=cm.hot, linewidth=0)
    plt.colorbar()
    print "done"

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$\\varphi(x,y)$")

    full_fname = "plots/" + filename
    print "Saving contour plot to file '{}'... ".format(full_fname),
    plt.savefig(full_fname)
    print "done"

def plot_vector(num_x, num_y, spacing, grid, filename="vector.eps"):
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
    plt.colorbar()
    print "done"

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$\mathbf{E}(x,y)$")

    full_fname = "plots/" + filename
    print "Saving vector plot to file '{}'... ".format(full_fname),
    plt.savefig(full_fname)
    print "done"
