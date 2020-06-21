'''
Some hacks / hooks on Taichi to make Taichi GLSL work
'''

import taichi as ti


def _deco_fix(old_deco):
    def decorator(foo):
        from functools import wraps
        decorated = old_deco(foo)

        @wraps(foo)
        def wrapped(*args, **kwargs):
            return decorated(*args, **kwargs)

        return wrapped

    return decorator


# A hotfix for taichi<0.6.11 not preserving function info.
# We needs this hijack function to make documentation strings work.
# We can remove this after taichi-dev/taichi#1233 merged in v0.6.11.
if ti.__version__ < (0, 6, 11):
    ti.func = _deco_fix(ti.func)

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
