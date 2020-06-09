import taichi as ti


def vec(*xs):
    return ti.Vector(xs)


def mat(*xs):
    return ti.Matrix(xs)
