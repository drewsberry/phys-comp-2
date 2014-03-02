# Library imports
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot(num_x, num_y, spacing, grid):
    # Use matplotlib.pyplot to create 3D plots of potential field.

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

    fig2 = plt.figure()
    cont_plot = plt.contourf(X, Y, grid.transpose(), 100, rstride=1, cstride=1, 
        cmap=cm.hot, linewidth=0)
    plt.colorbar()

    plt.xlabel("$x$")
    plt.ylabel("$y$")
    plt.title("$\\varphi(x,y)$")

    plt.savefig("contour.eps")
