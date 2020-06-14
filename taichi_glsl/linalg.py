'''
GLSL-alike linear algebra helper functions / aliases.
'''

import taichi as ti
from .common import ti_func


def vec(*xs):
    return ti.Vector(xs)


def mat(*xs):
    return ti.Matrix(xs)


@ti_func
def normalize(x):
    return x.normalized()


@ti_func
def dot(a, b):
    return a.dot(b)


@ti_func
def cross(a, b):
    return a.cross(b)


@ti_func
def outerProduct(a, b):
    return a.outer_product(b)


@ti_func
def length(x):
    return x.norm()


@ti_func
def distance(a, b):
    return (a - b).norm()


def shuffle(a, *indices):
    ret = []
    for i in indices:
        t = a.subscript(i)
        ret.append(t)
    return ti.Vector(ret)
