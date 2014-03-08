# Library imports
from __future__ import division
import argparse
import numpy as np
from numpy import linalg as la
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import types
import sys

# Custom libraries
import diffusion_evolve as dfe
import plotting

from matplotlib import cm

def evolve_anim(rod, xnum, pref_inv, ims, fig):
    
    rod[:,0] = 1273.15
    rod[:,xnum-1] = 273.15

    rod_new = rod.dot(pref_inv)
    # Faster than using np.solve(a,b), because inverse already calculated

    cont_plot = plt.contourf(X, Y, rod_new, 100, rstride=1, cstride=1,
        cmap=cm.hot)

    # Duck punch from matplotlib mailing list
    def setvisible(self,vis):
        for c in self.collections: c.set_visible(vis) 
    cont_plot.set_visible = types.MethodType(setvisible,cont_plot,None) 
    cont_plot.axes = plt.gca() 
    cont_plot.figure = fig

    ims.append([cont_plot])

    return rod_new

xnum = 52
width = 5
spacing = 0.1
alpha = 23e-6
delta_t = 10.0
h = 0.01
rod = np.zeros((width, xnum))
rod.fill(293.15)

prefactor = np.zeros((xnum, xnum))
for i in range(xnum):
    for j in range(xnum):
        if i == j:
            prefactor[i,j] = 1 + 2*alpha*delta_t / h**2
        if i == j-1 or i == j+1:
            prefactor[i,j] = - alpha*delta_t / h**2
prefactor[0,0] = 1 + alpha*delta_t / h**2
prefactor[xnum-1,xnum-1] = 1 + alpha*delta_t / h**2
# The bottom and top boundary nodes only average over one neighbour at same
# point on length

pref_inv = la.inv(prefactor)

ims = []

x = np.linspace(0, xnum*h, xnum)
y = np.linspace(0, width*h, width)    
X, Y = np.meshgrid(x,y)

fig = plt.figure(figsize=(3,10))
fig.suptitle("$\\phi(x,t)$")

num_frames = 1000
for frame in range(num_frames):
    rod = evolve_anim(rod, xnum, pref_inv, ims, fig)

    sys.stdout.flush()
    sys.stdout.write("\rNumber of frames completed: %5d / %5d;" %
                     (frame+1, num_frames))

print
print "Producing animation."
rod_anim = anim.ArtistAnimation(fig, ims, interval=1, blit=False)
print "Completed."

print "Saving as file."
rod_anim.save("multimedia/rod_anim.mp4")
print "Completed."