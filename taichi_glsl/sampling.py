'''
Some helper functions in processing fields & images.
'''

import taichi as ti
import taichi_glsl as ts

from .odop import TaichiClass

D = ts.vec(1, 0, -1)


@ti.func
def clampSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    P = ts.clamp(P, 0, shape - 1)
    return field[P]


@ti.func
def blackSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    ret = field[P] * 0
    if all(0 <= P and P < shape):
        ret = field[P]
    return ret


@ti.func
def whiteSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    ret = field[P] * 0 + 1
    if all(0 <= P and P < shape):
        ret = field[P]
    return ret


@ti.func
def nearestSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    P = int(ts.round(ts.clamp(P, 0, shape - 1)))
    return field[P]


@ti.func
def linearSample(field: ti.template(), P):
    I = int(P)
    x = ts.fract(P)
    y = 1 - x
    return (clampSample(field, I + D.xx) * x.x * x.y +
            clampSample(field, I + D.xy) * x.x * y.y +
            clampSample(field, I + D.yy) * y.x * y.y +
            clampSample(field, I + D.yx) * y.x * x.y)


@ti.func
def superSample2x2(fieldFunc: ti.template(), P):
    return (fieldFunc(P + 0.5 * D.yy) + fieldFunc(P + 0.5 * D.yz) +
            fieldFunc(P + 0.5 * D.zz) + fieldFunc(P + 0.5 * D.zy)) * 0.25


@ti.func
def vgridDivergence(field: ti.template(), I):
    return (clampSample(field, I + D.xy).x + clampSample(field, I + D.yx).y -
            clampSample(field, I + D.xz).x - clampSample(field, I + D.zx).y)


@ti.func
def vgridGradient(field: ti.template(), I):
    return ts.vec2(
        clampSample(field, I + D.yx) - clampSample(field, I + D.zx),
        clampSample(field, I + D.xy) - clampSample(field, I + D.xz))


@ti.func
def vgridSumAround(field: ti.template(), I):
    return (clampSample(field, I + D.yx) + clampSample(field, I + D.zx) +
            clampSample(field, I + D.xy) + clampSample(field, I + D.xz))


bilerp = linearSample
