'''
Some helper functions in processing fields & images.
'''

import taichi as ti
import taichi_glsl as ts

from .odop import TaichiClass

D = ts.vec(1, 0, -1)


@ti.func
def sample(field: ti.template(), P):
    '''
    Sampling a field with indices clampped into the field shape.

    :parameter field: (Tensor)
        Specify the field to sample.

    :parameter P: (Vector)
        Specify the index in field.

    :return:
        The return value is calcuated as::

            P = clamp(P, 0, vec(*field.shape) - 1)
            return field[int(P)]
    '''
    shape = ti.Vector(field.shape)
    P = ts.clamp(P, 0, shape - 1)
    return field[int(P)]


@ti.func
def dflSample(field: ti.template(), P, dfl):
    '''
    Sampling a field, when indices out of the field shape, return the given default value.

    :parameter field: (Tensor)
        Specify the field to sample.

    :parameter P: (Vector)
        Specify the index in field.

    :parameter dfl: (with the same type of field)
        Specify the index in field.

    :return:
        The return value is calcuated as::

            return field[int(P)] if 0 <= P < vec(*field.shape) else dfl
    '''
    shape = ti.Vector(field.shape)
    inside = 0 <= P < shape
    return field[int(P)] if inside else dfl


@ti.func
def bilerp(field: ti.template(), P):
    '''
    Bilinear sampling an 2D field with a real index.

    :parameter field: (2D Tensor)
        Specify the field to sample.

    :parameter P: (2D Vector of float)
        Specify the index in field.

    :note:
        If one of the element to be accessed is out of `field.shape`, then
        `bilerp` will automatically do a clamp for you, see :func:`sample`. 

    :return:
        The return value is calcuated as::

            I = int(P)
            x = fract(P)
            y = 1 - x
            return (sample(field, I + D.xx) * x.x * x.y +
                    sample(field, I + D.xy) * x.x * y.y +
                    sample(field, I + D.yy) * y.x * y.y +
                    sample(field, I + D.yx) * y.x * x.y)

        .. where D = vec(1, 0, -1)
    '''
    I = int(P)
    x = ts.fract(P)
    y = 1 - x
    return (sample(field, I + D.xx) * x.x * x.y +
            sample(field, I + D.xy) * x.x * y.y +
            sample(field, I + D.yy) * y.x * y.y +
            sample(field, I + D.yx) * y.x * x.y)


@ti.func
def trilerp(field: ti.template(), P):
    '''
    Tilinear sampling an 3D field with a real index.

    :parameter field: (3D Tensor)
        Specify the field to sample.

    :parameter P: (3D Vector of float)
        Specify the index in field.

    :note:
        If one of the element to be accessed is out of `field.shape`, then
        `Tilerp` will automatically do a clamp for you, see :func:`sample`.

        Syntax ref : https://en.wikipedia.org/wiki/Trilinear_interpolation.

    :return:
        The return value is calcuated as::

            I = int(P)
            w0 = ts.fract(P)
            w1 = 1.0 - w0
            c00 = ts.sample(field, I + ts.D.yyy) * w1.x + ts.sample(field, I + ts.D.xyy) * w0.x
            c01 = ts.sample(field, I + ts.D.yyx) * w1.x + ts.sample(field, I + ts.D.xyx) * w0.x
            c10 = ts.sample(field, I + ts.D.yxy) * w1.x + ts.sample(field, I + ts.D.xxy) * w0.x
            c11 = ts.sample(field, I + ts.D.yxx) * w1.x + ts.sample(field, I + ts.D.xxx) * w0.x

            c0 = c00 * w1.y + c10 * w0.y
            c1 = c01 * w1.y + c11 * w0.y

            return c0 * w1.z + c1 * w0.z

        .. where D = vec(1, 0, -1)
    '''
    I = int(P)
    w0 = ts.fract(P)
    w1 = 1.0 - w0

    c00 = ts.sample(field, I + ts.D.yyy) * w1.x + ts.sample(
        field, I + ts.D.xyy) * w0.x
    c01 = ts.sample(field, I + ts.D.yyx) * w1.x + ts.sample(
        field, I + ts.D.xyx) * w0.x
    c10 = ts.sample(field, I + ts.D.yxy) * w1.x + ts.sample(
        field, I + ts.D.xxy) * w0.x
    c11 = ts.sample(field, I + ts.D.yxx) * w1.x + ts.sample(
        field, I + ts.D.xxx) * w0.x

    c0 = c00 * w1.y + c10 * w0.y
    c1 = c01 * w1.y + c11 * w0.y

    return c0 * w1.z + c1 * w0.z


@ti.func
def superSample2x2(fieldFunc: ti.template(), P, dx=1):
    dD = dx / 2 * D
    return (fieldFunc(P + dD.yy) + fieldFunc(P + dD.yz) +
            fieldFunc(P + dD.zz) + fieldFunc(P + dD.zy)) * 0.25
