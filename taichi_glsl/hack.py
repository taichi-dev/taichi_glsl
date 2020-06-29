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
