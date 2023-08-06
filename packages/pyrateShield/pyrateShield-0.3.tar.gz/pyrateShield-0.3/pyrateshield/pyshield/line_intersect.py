# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 09:06:55 2015

Functions to find point of intersection and angle of intersection between
two lines
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import time
#number of significant digits (rounding)
SIG_DIGITS = 6

def sci_round(x, sig=SIG_DIGITS):
    """Scientific rounding

       x:                 float to be rounded
       sig = SIG_DIGITS:  Number of significant digits """
    x = np.asarray(x)
    p = SIG_DIGITS
    x_positive = np.where(np.isfinite(x) & (x != 0), np.abs(x), 10**(p-1))
    mags = 10 ** (p - 1 - np.floor(np.log10(x_positive)))
    return np.round(x * mags) / mags

    # if x == 0:  # special case, prevent taking log of zero
    #     return x
    # else:    # round
    #     return np.round(x, sig-int(math.floor(math.log10(abs(x))))-1)

def intersect_line(L0, L1):
    """ calculates the intersects of two lines

        L0 and L1: Lines specified by ((x0, y0), (x1, y1))

        - function returns the coordinataes of the intersection
          between both lines (px, py)
        - function returns an empty tuple if no intersection is found
        function returns (NaN, NaN) if lines are parallel
    """

    # unwrap lines


    x = [L0[0][0], L0[1][0], L1[0][0], L1[1][0]]
    y = [L0[0][1], L0[1][1], L1[0][1], L1[1][1]]


    #calculate denominator
    s1_x = x[1] - x[0]
    s1_y = y[1] - y[0]

    s2_x = x[3] - x[2]
    s2_y = y[3] - y[2]

    den = (-s2_x * s1_y + s1_x * s2_y)


    # if denominator is zero lines are parallel return NaN
    if sci_round(den) == 0:
        return (np.NAN, np.NAN)

    # parameterize line
    s = (-s1_y * (x[0] - x[2]) + s1_x * (y[0] - y[2])) / den
    t = (s2_x * (y[0] - y[2]) - s2_y * (x[0] - x[2])) / den

    # check if intersection lies on line pieces
    if (s >= 0) & (s <= 1) & (t >= 0) & (t <= 1):
        # calculate the intersection and return
        i_x = x[0] + (t * s1_x)
        i_y = y[0] + (t * s1_y)

        return (sci_round(i_x), sci_round(i_y))

    # lines not parallel but no intersection found on finite lines
    return (None, None)

def angle_between_lines(L0, L1):
    """ Angle in radians between two lines

        L0 and L1: Lines specified by ((x0, y0), (x1, y1))

        Even if both lines don't intersect the angle is returned.
    """

    L0 = np.asarray(L0)
    L1 = np.asarray(L1)

    if L0.ndim == 3 and L1.ndim == 2:
        L1 = np.stack([L1] * L0.shape[2], axis=2)

    elif L0.ndim == 2 and L1.ndim == 3:
        L0 = np.stack([L0] * L1.shape[2], axis=2)

    if L0.ndim == 2:
        L0 = np.expand_dims(np.asarray(L0),2)
    if L1.ndim == 2:
        L1 = np.expand_dims(np.asarray(L1),2)

    v0 = L0[1, :, :] - L0[0, : :]
    v1 = L1[1, :, :] - L1[0, : :]

    l0 = np.sqrt((v0[0, :]**2 + v0[1, :]**2))
    l1 = np.sqrt((v1[0, :]**2 + v1[1, :]**2))
    

    n0 = v0 / np.stack([l0, l0])
    n1 = v1 / np.stack([l1, l1])
    
   
    angle = np.arccos(n0[0, :] * n1[0,:] + n0[1, :] * n1[1,:])

    

    # #define vector direction
    # v0 = np.abs(L[1]-L[0])

    # n = v0.shape[1] if v0.ndim == 2 else 1

    # if n > 1:
    #     v1 = np.repeat(np.asarray([0, 1]), n, axis=0).reshape(v0.shape)


    # #normalize vectors
    # n0 = v0/np.linalg.norm(v0)
    # n1 = v1/np.linalg.norm(v1)

    # #prevent rounding errors, acos returns an error for values > 1
    # inprod = sci_round(n0[0, :] * n1[0, :] + n0[1,:] + n1[1,:])

    # #calculate angles
    # angle = np.arccos(inprod)

    return sci_round(angle)

def intersect_lines(lines, timer=False):
    """ Calculate all intersections of a  list of lines

        lines:  A list of lines. Each line is defined by two points
                line = ((x0, y0), (x1, y1))"""
    if timer: start_time = time.time()
    intersect = []
    for i in range(0, len(lines)):
        for j in range(i+1, len(lines)):
            p = intersect_line(lines[i], lines[j])
            if not None in p:
                if not np.any(np.isnan(p)):
                    intersect.append(p)
    if timer: end_time = time.time()
    if timer: print(str((end_time-start_time) * 1000) + 'ms')
    return tuple(intersect)

def plot_lines(lines):
    """ Plot a list of lines with points of intersection

        lines:  A list of lines. Each line is defined by two points
                line = ((x0, y0), (x1, y1))"""

    for line in lines:
        plt.plot(line[:, 0], line[:, 1])

    intersects = intersect_lines(lines, timer=True)

    for intersect in intersects:
        plt.plot(*intersect, ' ro')
    return

def rand_line(bounds=((0, 0), (1, 1))):
    """ Return a random line

         bounds: ((xmin, ymin), (xmax, ymax)) the line must be within these
                  bounds."""
    return np.array((rand_point(bounds), rand_point(bounds)))


def rand_point(bounds=((0, 0), (1, 1))):
    """ Return a random point.

        bounds:  ((xmin, ymin), (xmax, ymax)) the line point be within these
                  bounds."""
    xi = random.random() * (bounds[1][0]-bounds[0][0]) + bounds[0][0]
    yi = random.random() * (bounds[1][0]-bounds[0][0]) + bounds[0][0]
    return (xi, yi)

def unit_vector(vector):
    return vector / np.linalg.norm(vector)



def get_angle(poly, point, line):
    x, y = poly

    sx = point[0] * np.ones(x.shape)
    sy = point[1] * np.ones(x.shape)

    L0 = np.stack(((x, y), (sx, sy)))
    L1 = np.asarray(line)

    return angle_between_lines(L0, L1)








    # angles = get_angle(ppoints, source, line)


    # angle_map = np.zeros(imshape)

    # angle_map[ppoints[0], ppoints[1]] = angles

    # plt.imshow(angle_map)#, clim=[0,2])
    # plt.colorbar()




