'''
Some hacks / hooks on Taichi to make Taichi GLSL work
'''

import taichi as ti


# A hotfix for taichi<=0.6.10 not preserving function info.
# We needs this hijack function to make documentation strings work.
# We can remove this after taichi-dev/taichi#1233 merged in v0.6.11.
def _deco_fix(old_deco):
    def decorator(foo):
        from functools import wraps
        decorated = old_deco(foo)

        @wraps(foo)
        def wrapped(*args, **kwargs):
            return decorated(*args, **kwargs)

        return wrapped

    return decorator


ti.func = _deco_fix(ti.func)
