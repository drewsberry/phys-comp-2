# Library imports
import numpy as np

try:
    import matplotlib
    import matplotlib.pyplot as plt

    from matplotlib import cm
    from mpl_toolkits.mplot3d import Axes3D
except ImportError as e:
    print "Error importing matplotlib library. You will not be able to use the "\
          "'-p' or '--plot' option."
    print "Error message: {}".format(e)

def plot_surf(num_x, num_y, spacing, grid):
    # Use matplotlib.pyplot to create 3D surf plot of potential field.

    x = np.linspace(0, num_x*spacing, num_x)
    y = np.linspace(0, num_y*spacing, num_y)  
    X, Y = np.meshgrid(x,y)

    fig = plt.figure()

    surf_axes = fig.gca(projection='3d')
    surf_plot = surf_axes.plot_surface(X, Y, grid.transpose(), rstride=1, cstride=1,
        cmap=cm.hot, linewidth=0, antialiased=True)

    surf_axes.set_xlabel("$x$")
    surf_axes.set_ylabel("$y$")
    surf_axes.set_title("$\\varphi(x,y)$")

    plt.savefig("surf.eps")

def plot_contour(num_x, num_y, spacing, grid):
    # Use matplotlib to plot contours of potential field.

    x = np.linspace(0, num_x*spacing, num_x)
    y = np.linspace(0, num_y*spacing, num_y)  
    X, Y = np.meshgrid(x,y)

    fig = plt.figure()

    cont_plot = plt.contourf(X, Y, grid.transpose(), 100, rstride=1, cstride=1, 
        cmap=cm.hot, linewidth=0)
    plt.colorbar()

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$\\varphi(x,y)$")

    plt.savefig("contour.eps")

def plot_vector(num_x, num_y, spacing, grid):
    # Plot the vector gradient of potential field using arrows.

    Y, X = np.mgrid[0:num_x*spacing:complex(0,num_x),
                    0:num_y*spacing:complex(0,num_y)]

    vector_u, vector_v = np.gradient(grid.transpose())

    vector_u = np.zeros((num_x, num_y)) - vector_u
    vector_v = np.zeros((num_x, num_y)) - vector_v

    magnitude = np.sqrt(vector_u*vector_u + vector_v*vector_v)

    fig = plt.figure()

    lw = 5*magnitude/magnitude.max()
    stream_plot = plt.streamplot(X, Y, vector_v, vector_u, color=magnitude, 
                                 linewidth=lw, cmap=cm.hot)
    plt.colorbar()

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$\mathbf{E}(x,y)$")

    plt.savefig("vector.eps")
