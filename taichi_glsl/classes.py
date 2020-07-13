import taichi as ti
import taichi_glsl as tl


class Complex(tl.TaichiClass, ti.TaichiOperations):
    '''
    Complex number support in Taichi GLSL

    :note:
        `complex * complex` is the **element-wise** multiplication.
        Use `complex @ complex` if you mean to use complex number multiplication.
    '''
    def __init__(self, x, y=None):
        '''Construct a complex from a vector / two scalars'''
        if y is None:
            if isinstance(x, (ti.Matrix, Complex)):
                x, y = x.entries
            else:
                y = x * 0
        self.entries = [x, y]

    @property
    def x(self):
        '''Real part of the complex'''
        return self.entries[0]

    re = x

    @property
    def y(self):
        '''Imaginary part of the complex'''
        return self.entries[1]

    im = y

    @property
    def mag2(self):
        '''Squared magnitude of the complex'''
        return self.x**2 + self.y**2

    @property
    def mag(self):
        '''Magnitude of the complex'''
        return ti.sqrt(self.mag2)

    @property
    def ang(self):
        '''Phase angle of the complex'''
        return ti.atan2(self.y, self.x)

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

    # TODO: intergrate into __mul__?
    def __matmul__(a, b):
        '''Multiply two complex numbers'''
        # XXX: SSA violation on random?
        if not isinstance(b, Complex):
            b = Complex(b)
        return Complex(a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x)

    __rmatmul__ = __matmul__


# TODO: add Affine and Subtensor
