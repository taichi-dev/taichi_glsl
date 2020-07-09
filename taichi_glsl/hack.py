'''
Some hacks / hooks on Taichi to make Taichi GLSL work
'''

import taichi as ti


# Make ti.static support Taichi classes:
ti_static = ti.static


def _ts_static(x, *xs):
    if len(xs) == 0:
        return x

    return [x] + xs


ti.static = _ts_static

# Get rid of the annoying deprecation warnings:
__import__('warnings').filterwarnings('ignore')

# Get rid of `maybe you want to use a.fill(b)?` limitation.
_old_element_wise_binary = ti.Matrix.element_wise_binary


def _new_element_wise_binary(self, foo, other):
    if foo.__name__ == 'assign':
        foo.__name__ = 'dummy_assign'
    return _old_element_wise_binary(self, foo, other)


ti.Matrix.element_wise_binary = _new_element_wise_binary


# Add ti.Matrix.product method:
@ti.func
def _vector_product(self: ti.template()):
    ret = self[0]
    for i in ti.static(range(1, self.n)):
        ret *= self[i]
    return ret


ti.Matrix.product = _vector_product
