'''
Some internal tools used commonly in Taichi GLSL library.
'''

import taichi as ti

# A hotfix for taichi<=0.6.10 not preserving function info.
# We needs this hijack function to make documentation strings work.
# We can remove this after taichi-dev/taichi#1233 merged in v0.6.11.
def ti_func(foo):
    from functools import wraps
    decorated = ti.func(foo)

    @wraps(foo)
    def wrapped(*args):
        return decorated(*args)

    return wrapped
