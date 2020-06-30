'''
Some hacks / hooks on Taichi to make Taichi GLSL work
'''

import taichi as ti

if not hasattr(ti.Vector, 'var'):
    ti.Vector.var = ti.Vector

# Make ti.static support Taichi classes:
ti_static = ti.static


def _ts_static(x, *xs):
    def _static(x):
        if ti.is_taichi_class(x):
            return x
        else:
            return ti_static(x)

    if len(xs) == 0:
        return _static(x)
    return [_static(x)] + [_static(_) for _ in xs]


ti.static = _ts_static

# Get rid of the annoying deprecation warnings:
__import__('warnings').filterwarnings('ignore')

# Get rid of `maybe you want to use a.fill(b)?` limitation.
_old_element_wise_binary = ti.Matrix.element_wise_binary


def _new_element_wise_binary(self, foo, other):
    if foo.__name__ == 'assign':
        foo.__name__ == '_assign'
    return _old_element_wise_binary(self, foo, other)


ti.Matrix.element_wise_binary = _new_element_wise_binary


@ti.func
def _vector_product(self: ti.template()):
    ret = self[0]
    for i in ti.static(range(1, self.n)):
        ret *= self[i]
    return ret


ti.Matrix.product = _vector_product
