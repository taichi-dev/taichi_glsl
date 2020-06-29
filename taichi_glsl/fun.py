'''
(Experimental) Some stuffs for fun!
'''

import taichi as ti


@ti.func
def _inside(p, c, r):
    return (p - c).norm_sqr() <= r * r


@ti.func
def insideTaichi(p):
    p = ti.Vector([0.5, 0.5]) + (p - ti.Vector([0.5, 0.5])) * 1.11
    ret = -1
    if not _inside(p, ti.Vector([0.50, 0.50]), 0.55):
        if ret == -1:
            ret = 0
    if not _inside(p, ti.Vector([0.50, 0.50]), 0.50):
        if ret == -1:
            ret = 1
    if _inside(p, ti.Vector([0.50, 0.25]), 0.09):
        if ret == -1:
            ret = 1
    if _inside(p, ti.Vector([0.50, 0.75]), 0.09):
        if ret == -1:
            ret = 0
    if _inside(p, ti.Vector([0.50, 0.25]), 0.25):
        if ret == -1:
            ret = 0
    if _inside(p, ti.Vector([0.50, 0.75]), 0.25):
        if ret == -1:
            ret = 1
    if p[0] < 0.5:
        if ret == -1:
            ret = 1
    else:
        if ret == -1:
            ret = 0
    return ret
