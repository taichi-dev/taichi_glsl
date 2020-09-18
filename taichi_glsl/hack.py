'''
Some hacks / hooks on Taichi to make Taichi GLSL work
'''

import taichi as ti

# Make ti.static support Taichi classes:
ti_static = ti.static


def _ts_static(x, *xs):
    if len(xs) == 0:
        return x

    return [x] + list(xs)


ti.static = _ts_static

## Get rid of the annoying deprecation warnings:
__import__('warnings').filterwarnings('ignore')

# Get rid of `maybe you want to use a.fill(b)?` limitation.
_old_element_wise_binary = ti.Matrix.element_wise_binary


def _new_element_wise_binary(self, foo, other):
    if foo.__name__ == 'assign':
        foo.__name__ = 'dummy_assign'
    return _old_element_wise_binary(self, foo, other)


ti.Matrix.element_wise_binary = _new_element_wise_binary


# Add ti.Matrix.product method:
@ti.pyfunc
def _vector_product(self: ti.template()):
    ret = self[0]
    for i in ti.static(range(1, self.n)):
        ret *= self[i]
    return ret


ti.Matrix.product = _vector_product


# Add ti.Matrix.{L,L2,N,T,det,inv,tr} property:
def _vector_L(self):
    return self.norm()


def _vector_L2(self):
    return self.norm_sqr()


def _vector_N(self):
    return self.normalized()


def _matrix_T(self):
    return self.transpose()


def _matrix_det(self):
    return self.determinant()


def _matrix_inv(self):
    return self.inverse()


def _matrix_tr(self):
    return self.trace()


ti.Matrix.L = property(_vector_L)
ti.Matrix.L2 = property(_vector_L2)
ti.Matrix.N = property(_vector_N)
ti.Matrix.T = property(_matrix_T)
ti.Matrix.det = property(_matrix_det)
ti.Matrix.inv = property(_matrix_inv)
ti.Matrix.tr = property(_matrix_tr)

# Add ti.pi and ti.tau:
import math

pi = math.pi
tau = math.tau
ti.pi = pi
ti.tau = tau