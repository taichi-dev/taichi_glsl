import taichi as ti
import taichi_glsl as tl


class Complex(tl.TaichiClass, ti.TaichiOperations):
    def __init__(self, x, y=0.0):
        self.entries = [x, y]

    @property
    def x(self):
        return self.entries[0]

    @property
    def y(self):
        return self.entries[1]

    @classmethod
    def _var(cls, *args, **kwargs):
        x = ti.var(*args, **kwargs)
        y = ti.var(*args, **kwargs)
        return x, y

    def element_wise_unary(a, foo):
        return Complex(foo(a.x), foo(a.y))

    def element_wise_binary(a, foo, b):
        if not isinstance(b, Complex):
            b = Complex(b)
        return Complex(foo(a.x, b.x), foo(a.y, b.y))

    def element_wise_writeback_binary(a, foo, b):
        if ti.is_taichi_class(b):
            b = b.variable()
        if not isinstance(b, Complex):
            b = Complex(b)
        return Complex(foo(a.x, b.x), foo(a.y, b.y))

    def __ti_repr__(self):
        yield '('
        yield self.x
        yield ' + '
        yield self.y
        yield 'j'
        yield ')'

    def __matmul__(a, b):
        # XXX: SSA violation on random?
        if not isinstance(b, Complex):
            b = Complex(b)
        return Complex(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x)

    __rmatmul__ = __matmul__
