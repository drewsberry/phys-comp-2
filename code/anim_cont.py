from __future__ import division # Division always returns float

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import sys

# Custom libraries
import animation

num_x = 100
num_y = 100
h = 1/16

num_nodes = num_x*num_y

ims = []

x = np.linspace(0, num_x*h, num_x)
y = np.linspace(0, num_y*h, num_y)    
X, Y = np.meshgrid(x,y)

fig = plt.figure()
fig.suptitle("$\\varphi(x,y)$")

num_frames = 200
for frame in range(num_frames):
    sys.stdout.flush()
    sys.stdout.write("\r\t\t\t\t\t\t\t\t\t\tFrames completed: %5d / %5d" % 
                     (frame+1, num_frames))

    animation.laplace_anim_cont(num_x, num_y, "gauss-seidel", ims, fig, X, Y, 
                                frame=frame, boundary_cond="capacitor")

print "Iterations finished. Creating animation."
capacitor_anim = anim.ArtistAnimation(fig, ims, interval=100, blit=False)
plt.colorbar()
print "Animation made. Saving to file."

capacitor_anim.save("multimedia/cont_anim_new.mp4")
print "Animation saved to file as {filename}.".format(filename="cont_anim.mp4")
