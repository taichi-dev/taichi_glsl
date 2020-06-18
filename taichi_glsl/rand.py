'''
Pseudo-random number or noise generators.
'''

import taichi as ti
import math


def rand():
    '''
    Generate a random floating number distributed evenly in range [0, 1].

    :return:
        The return value a pseudo-random floating number in range [0, 1].

    .. note::

        Depending on Taichi backend design, the generated random number
        may have the **same seed** on start up. And Taichi doesn't provide
        any way to set a random seed yet, so does Taichi GLSL.
    '''

    return ti.random()


@ti.func
def randInt(a, b):
    '''
    Generate a random integer in range [a, b], including both end points.

    :parameter a:
        Specify the start point of range.
    :parameter b:
        Specify the end point of range.

    :return:
        The return value is calculated as `ti.random(ti.i32) % (b - a) + a`.

    :note:
        This means randInt could not fullfill its promise of "distributed
        evenly" when (b - a) is large (at the scalr of INT_MAX).
    '''

    return ti.random(ti.i32) % (b - a) + a


def randND(n):
    '''
    Generate a n-D random vector in a n-D cube ([0, 1]).
    The return value is a n-D vector, each comonment is a random floating
    number in range [0, 1] generated independently.

    :parameter n:
        Specify the dimension of random vector to generate.

    :return:
        The return value is calculated as `vec(rand() for _ in range(n))`.
    '''

    return ti.Vector([rand() for _ in range(n)])


@ti.func
def randRange(a=0, b=1):
    '''
    Generate random floating numbers in range [a, b].
    If `a` and `b` are n-D vectors, then the return value will also be a
    n-D vector, whose i-th component is a random number distributed evenly
    in range [a[i], b[i]], each comonment is generated independently.

    :parameter a:
        Specify the start point of range.
    :parameter b:
        Specify the end point of range.

    :return:
        The return value is calculated as `a + rand() * (b - a)`.
    '''
    return a + rand() * (b - a)


@ti.func
def randNDRange(a, b):
    '''
    Generate a n-D random vector in a n-D cube.
    `a` and `b` should be n-D vectors. The return value is also a n-D
    vector, whose i-th component is a random number distributed evenly
    in range [a[i], b[i]], each componment is generated independently.

    :parameter a:
        Specify the staring point / coordinate of cube.
    :parameter b:
        Specify the ending point / coordinate of cube.

    :return:
        The return value is calculated as `a + randND((b - a).n) * (b - a)`.
    '''
    c = b - a
    return a + randND(c.n) * c


@ti.func
def randUnit2D():
    '''
    Generate a 2-D random unit vector whose length is equal to 1.0.
    The return value is a 2-D vector, whose tip distributed evenly
    **on the border** of a unit circle.

    :return:
        The return value is computed as::

            a = rand() * math.tau
            return vec(ti.cos(a), ti.sin(a))
    '''
    a = rand() * math.tau
    return ti.Vector([ti.cos(a), ti.sin(a)])


@ti.func
def randSolid2D():
    '''
    Generate a 2-D random unit vector whose length is <= 1.0.
    The return value is a 2-D vector, whose tip distributed evenly
    **inside** a unit circle.

    :return:
        The return value is computed as::

            a = rand() * math.tau
            r = sqrt(rand())
            return vec(cos(a), sin(a)) * r
    '''
    a = rand() * math.tau
    r = ti.sqrt(rand())
    return ti.Vector([ti.cos(a), ti.sin(a)]) * r


@ti.func
def randUnit3D():
    '''
    Generate a 3-D random unit vector whose length is equal to 1.0.
    The return value is a 3-D vector, whose tip distributed evenly
    **on the surface** of a unit sphere.
    '''
    from .linalg import vec3
    u = randUnit2D()
    s = rand() * 2 - 1
    c = ti.sqrt(1 - s**2)
    return vec3(c * u, s)
