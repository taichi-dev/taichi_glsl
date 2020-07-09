'''
Some often-used SPH smoother kernels.
'''

import taichi as ti


@ti.func
def spiky(r, h):
    '''
    (h - r)**3
    '''
    return (h - r)**3


@ti.func
def poly6(r, h):
    '''
    (h**2 - r**2)**3
    '''
    return (h**2 - r**2)**3


@ti.func
def dspiky(r, h):
    '''
    -3 * (h - r)**2
    '''
    return -3 * (h - r)**2


@ti.func
def dpoly6(r, h):
    '''
    -6 * r * (h**2 - r**2)**2
    '''
    return -6 * r * (h**2 - r**2)**2
