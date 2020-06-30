'''
(Experimental) OpenGL-alike view transformations.
'''

import taichi as ti


def _tuple_to_vector(x):
    if len(x) != 1 or not isinstance(x[0], Matrix):
        x = ti.Matrix(x)
    return x


def view(image, *indices):
    indices = _tuple_to_vector(indices)
    return indices / image.shape()


def tex(image, *coors):
    coors = _tuple_to_vector(coors)
    return indices / image.shape()
