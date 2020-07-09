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


@ti.host_arch_only
def test_subscript_0d():
    c = Complex.var(ti.f32, ())
    
    @ti.kernel
    def func() -> ti.f32:
        return c[None].x + c[None].y

    # tl.TaichiClass.Proxy W.I.P.
    c.x[None] = 2
    c.y[None] = 11
    assert func() == 13


@ti.host_arch_only
def test_subscript_1d():
    c = Complex.var(ti.f32, 4)
    
    @ti.kernel
    def func(i: ti.i32) -> ti.f32:
        return c[i].x + c[i].y

    c.x[2] = 2
    c.x[1] = 11
    c.y[2] = 7
    assert func(2) == 9


@ti.host_arch_only
def test_loop_range_1d():
    c = Complex.var(ti.f32, 4)
    count = ti.var(ti.i32, ())
    
    @ti.kernel
    def func() -> ti.f32:
        res = 0.0
        for i in c:
            count[None] += i
            res += c[i].x
        return res

    c.x[2] = 2
    c.x[1] = 11
    c.y[2] = 7
    c.y[2] = 8
    assert func() == 13
    assert count[None] == 6


@ti.host_arch_only
def test_loop_range_2d():
    c = Complex.var(ti.f32, (2, 4))
    count = ti.var(ti.i32, ())
    
    @ti.kernel
    def func() -> ti.f32:
        res = 0.0
        for i, j in c:
            count[None] += j
            res += c[i, j].x
        return res

    c.x[0, 2] = 2
    c.x[1, 1] = 11
    c.x[1, 2] = 8
    c.y[1, 0] = 7
    c.y[1, 2] = 8
    assert func() == 21
    assert count[None] == 12


@ti.host_arch_only
def test_loop_atomic_add():
    c = Complex.var(ti.f32, 4)
    r = Complex.var(ti.f32, ())
    
    @ti.kernel
    def func():
        r[None] = 0.0
        for i in c:
            r[None] += c[i]

    c.x[2] = 2
    c.x[1] = 11
    c.y[2] = 7
    c.y[3] = 13
    func()
    assert r.x[None] == 13
    assert r.y[None] == 20


@ti.host_arch_only
def test_loop_matmul():
    c = Complex.var(ti.f32, 2)
    r = Complex.var(ti.f32, ())
    
    @ti.kernel
    def func():
        r[None] = Complex(1.0, 0.0)
        for i in ti.static(range(2)):
            print('r[None] =', r[None])
            print('c[i] =', c[i])
            print('b', i, r[None] @ c[i])
            r[None] = r[None] @ c[i]
            print('a', i, r[None])

    c.x[0] = 2
    c.y[0] = 7
    c.x[1] = 11
    c.y[1] = 13
    func()
    print('r', Complex(r.x[None], r.y[None]))
    assert r.x[None] == 2 * 11 - 7 * 13
    assert r.y[None] == 2 * 13 + 7 * 11
