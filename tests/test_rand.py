from taichi_glsl import *
from pytest import approx


def mean_approx_test(x, xmin, xmax, rel=1e-2):
    if not isinstance(x, np.ndarray):
        x = x.to_numpy()
    x = (x - xmin) / (xmax - xmin)
    for i in range(1, 4):
        assert (x**i).mean() == approx(1 / (i + 1), rel=rel)


@ti.host_arch_only
def test_rand():
    n = 1024**2
    x = array(float, n)

    @ti.kernel
    def fill():
        for i in x:
            x[i] = rand()

    fill()
    mean_approx_test(x, 0, 1)


@ti.host_arch_only
def test_rand_independent_product():
    n = 1024**2
    x = array(float, n)

    @ti.kernel
    def fill():
        for i in x:
            x[i] = rand() * rand()

    fill()
    assert x.to_numpy().mean() == approx(1 / 4, rel=1e-2)


@ti.host_arch_only
def test_rand_range():
    n = 1024**2
    a, b = 0.6, 1.4
    x = array(ti.f32, n)

    @ti.kernel
    def fill():
        for i in x:
            x[i] = randRange(a, b)

    fill()
    mean_approx_test(x, a, b)


@ti.host_arch_only
def test_rand_2d():
    n = 8192
    x = vec_array(2, float, n)

    @ti.kernel
    def fill():
        for i in x:
            x[i] = randND(2)

    fill()
    x = x.to_numpy()
    counters = [0 for _ in range(4)]
    for i in range(n):
        c = int(x[i, 0] < 0.5) * 2 + int(x[i, 1] < 0.5)
        counters[c] += 1

    for c in range(4):
        assert counters[c] / n == approx(1 / 4, rel=0.2)


@ti.host_arch_only
def test_rand_int():
    n = 1024**2
    a, b = 768, 1131
    x = array(float, n)

    @ti.kernel
    def fill():
        for i in x:
            x[i] = randInt(a, b)

    fill()
    mean_approx_test(x, a, b, rel=1e-1)


@ti.host_arch_only
def test_rand_unit_2d():
    n = 1024
    x = vec_array(2, float, n)

    @ti.kernel
    def fill():
        for i in x:
            x[i] = randUnit2D()

    fill()
    x = x.to_numpy()
    len = np.sum(x**2, axis=1)
    ang = np.arctan2(x[:, 1], x[:, 0])
    assert len == approx(np.ones(n))
    mean_approx_test(ang, -math.pi, math.pi, rel=4e-1)


test_rand_int()
