test#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 22:59:04 2018

@author: alaridatascience
"""

# -----------------------------------------------------------------------------
# From https://en.wikipedia.org/wiki/Minkowski–Bouligand_dimension:
#
# In fractal geometry, the Minkowski–Bouligand dimension, also known as
# Minkowski dimension or box-counting dimension, is a way of determining the
# fractal dimension of a set S in a Euclidean space Rn, or more generally in a
# metric space (X, d).
# -----------------------------------------------------------------------------
import scipy.misc
import numpy as np

def plot_traj(data,par,noshow):
    ''' Plot trajectory in data frame format'''
    x = data['longitude']
    y = data['latitude']
    xmin,xmax = min(x),max(x)
    ymin,ymax = min(y),max(y)
    fig = plt.figure()
    xrange,yrange = xmax-xmin,ymax-ymin
    plt.axis([xmin-0.01*xrange, xmax+0.01*xrange, ymin-0.01*yrange, ymax+0.01*yrange])
    if(par==1):
        plt.scatter(x,y)
    else:
        plt.plot(x,y)
    if(noshow==0): plt.show()
    return(fig)


a = fractal_dimension(K, 0.5)
p = plot_traj(taxi_999_traj,1)

def hausdorff_fractal_dimension(traj, threshold=0.2):
    ''' Compute the fractal dimension of a trajectory'''
  
    def boxcount(traj, k):
        S = np.add.reduceat(
            np.add.reduceat(traj, np.arange(0, traj.shape[0], k), axis=0),
                               np.arange(0, traj.shape[1], k), axis=1)

        # We count non-empty boxes
        return len(np.where((S > 0))[0] & (S < k*k)[0])


    # Transform Z into a binary array
    traj = (traj < threshold)

    # Minimal dimension of image
    p =traj.shape[0]

    # Greatest power of 2 less than or equal to p
    n = 2**np.floor(np.log(p)/np.log(2))

    # Extract the exponent
    n = int(np.log(n)/np.log(2))

    # Build successive box sizes (from 2**n down to 2**1)
    sizes = 2**np.arange(n, 1, -1)

    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        c = boxcount(Z, size)
        counts.append(c)
        
    co = np.asarray(counts)
    si = np.asarray(sizes)
    zerotest = co != 0
    co = np.extract(zerotest, co)
    si = np.extract(zerotest, si)

    # Fit the successive log(sizes) with log (counts)
    plt.scatter(np.log(si),np.log(co))
    coeffs = np.polyfit(np.log(si), np.log(co), 1)
    
    return(-coeffs[0])

i = plot_traj(test_traj,1)

frac_dims = [None]*len(trajectories_20)
for idx,tr in enumerate(trajectories_20):
    if(idx==100):
        break
    p = plot_traj(tr,1)
    picname = 'out'+str(idx)+'.png'
    #p.savefig(picname)
   # I = plt.imread(picname)/sizes[0]
   # if(np.isnan(I).any()=='False'):
   
    

#%% PLOTTING
xs = np.log(sizes)
ys = np.log(counts)
A = np.vstack([xs, np.ones(len(xs))]).T
m,b = np.linalg.lstsq(A, ys)[0]
def line(x): return m*x+b
ys = line(xs)
plt.plot(xs,ys)