import taichi as ti


def vec(*xs):
    return ti.Vector(xs)


def mat(*xs):
    return ti.Matrix(xs)


@ti.func
def normalize(x):
    return x.normalized()


@ti.func
def dot(a, b):
    return a.dot(b)


@ti.func
def cross(a, b):
    return a.cross(b)


@ti.func
def outerProduct(a, b):
    return a.outer_product(b)


@ti.func
def length(x):
    return x.norm()


@ti.func
def distance(a, b):
    return (a - b).norm()


def shuffle(a, *indices):
    ret = []
    for i in indices:
        t = a.subscript(i)
        ret.append(t)
    return ti.Vector(ret)
