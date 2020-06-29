'''
(Experimental) Some stuffs for fun!
'''

import taichi as ti
import taichi_glsl as ts


@ti.func
def _inside(p, c, r):
    return (p - c).norm_sqr() <= r * r


@ti.func
def imageTaichi(p, size=1):
    p = ti.Vector([0.5, 0.5]) + (p - ti.Vector([0.5, 0.5])) * 1.11 / size
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
    return 1 - ret


@ti.func
def imageChess(p, n=20):
    return (p // (1 / n)).sum() % 2


@ti.func
def imageGrid(p, n=20, tol=0.2):
    return ts.smoothstep(abs(ts.fract(p * n) - 0.5).min(), 0.0, tol)
