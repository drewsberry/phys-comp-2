# Library imports
from __future__ import division
import argparse
import numpy as np

# Custom libraries
import diffusion_evolve as dfe
import plotting
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import types
import sys

from matplotlib import cm

xnum = 52
width = 5
spacing = 0.1
alpha = 23e-6
delta_t = 10.0
h = 0.01
rod = np.zeros((xnum, width))

prefactor = np.zeros((xnum, xnum))
for i in range(xnum):
    for j in range(xnum):
        if i == j:
            prefactor[i,j] = 1 + 2*alpha*delta_t / h**2
        if i == j-1 or i == j+1:
            prefactor[i,j] = - alpha*delta_t / h**2

ims = []

x = np.linspace(0, xnum*h, xnum)
y = np.linspace(0, width*h, width)    
X, Y = np.meshgrid(x,y)

fig = plt.figure(figsize=(10,3))
fig.suptitle("$\\phi(x,t)$")

num_frames = 400
for frame in range(num_frames):
    rod = dfe.evolve(rod, xnum, prefactor)

    plt.xlabel("$x$")
    plt.ylabel("$y$")

    rod_plot = plt.contourf(X, Y, rod.transpose(), 100, rstride=1, cstride=1,
        cmap=cm.hot)

    # Duck punch from matplotlib mailing list
    def setvisible(self,vis):
        for c in self.collections: c.set_visible(vis) 
    rod_plot.set_visible = types.MethodType(setvisible,rod_plot,None) 
    rod_plot.axes = plt.gca() 
    rod_plot.figure = fig

    ims.append([rod_plot])

    sys.stdout.flush()
    sys.stdout.write("\rNumber of frames completed: %5d / %5d;" %
                     (frame+1, num_frames))

    # plotting.plot_contour(width, xnum+1, spacing, rod.transpose(),
    #                       filename="diff_cont_" + str(k))

print "Producing animation."
rod_anim = anim.ArtistAnimation(fig, ims, interval=100, blit=False)
plt.colorbar()
print "Completed."

print "Saving as file."
rod_anim.save("multimedia/rod_anim.mp4")
print "Completed."