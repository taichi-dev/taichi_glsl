from taichi_glsl import *
import pytest

test_range = [
    -1e3 + 0.1,
    -1e-4 + 1,
    -15.9,
    -1.501,
    -1.499,
    -1.0,
    -0.34,
    0.5,
    0.0,
    0.33,
    0.5,
    1.0,
    1.499,
    1.501,
    4.0,
    9.99,
    1e5,
]
test_range_2 = [
    (-1.0, 0.0),
    (-1.0, 0.5),
    (0.0, 0.5),
    (0.0, -1.0),
    (0.5, 1.0),
    (0.5, 1.5),
    (1e5, 0.0),
    (1e5, 0.5),
    (0.5, -1e5),
    (-3.5, 0.5),
]


@pytest.mark.parametrize('a', test_range)
def test_sign(a):
    @ti.kernel
    def calc(a: ti.f32) -> ti.f32:
        return sign(a)

    r = calc(a)
    if a > 0:
        assert r == 1
    elif a == 0:
        assert r == 0
    else:
        assert r == -1


@pytest.mark.parametrize('a', test_range)
def test_round(a):
    @ti.kernel
    def calc(a: ti.f32) -> ti.f32:
        return round(a)

    r = calc(a)
    # According to https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/round.xhtml:
    # round returns a value equal to the nearest integer to x. The fraction 0.5 will round in a direction chosen by the implementation, presumably the direction that is fastest. This includes the possibility that round(x) returns the same value as roundEven(x) for all values of x.
    # So our implementation could:     ts.round(0.5) = 1.0
    # However,                         np.round(0.5) = 0.0
    # So let's play a trick on it:
    assert r == pytest.approx(np.round(a + 1e-7))


@pytest.mark.parametrize('a', test_range)
def test_floor(a):
    @ti.kernel
    def calc(a: ti.f32) -> ti.f32:
        return floor(a)

    r = calc(a)
    assert r == pytest.approx(np.floor(a), rel=1e-3)


@pytest.mark.parametrize('a', test_range)
def test_fract(a):
    @ti.kernel
    def calc(a: ti.f32) -> ti.f32:
        return fract(a)

    r = calc(a)
    assert r == pytest.approx(a - np.floor(a), rel=1e-3)


@pytest.mark.parametrize('a',
                         [4e-2, 0.3, 0.8, 1.0, 1.55, 2.0, 4.2, 141.0, 1e3])
def test_inversesqrt(a):
    @ti.kernel
    def calc(a: ti.f32) -> ti.f32:
        return inversesqrt(a)

    r = calc(a)
    assert r == pytest.approx(a**-0.5, rel=1e-3)


@pytest.mark.parametrize('a', test_range)
def test_atan(a):
    @ti.kernel
    def calc(a: ti.f32) -> ti.f32:
        return atan(a)

    r = calc(a)
    assert r == pytest.approx(np.arctan(a))


@pytest.mark.parametrize('a,b', test_range_2)
def test_atan2(a, b):
    @ti.kernel
    def calc(a: ti.f32, b: ti.f32) -> ti.f32:
        return atan(a, b)

    r = calc(a, b)
    assert r == pytest.approx(np.arctan2(a, b))


@pytest.mark.parametrize('a,b', test_range_2)
def test_step(a, b):
    @ti.kernel
    def calc(a: ti.f32, b: ti.f32) -> ti.f32:
        return step(a, b)

    r = calc(a, b)
    if a < b:
        assert r == 1
    else:
        assert r == 0


@pytest.mark.parametrize('a,b', test_range_2)
def test_sign2(a, b):
    @ti.kernel
    def calc(a: ti.f32, b: ti.f32) -> ti.f32:
        return sign(a, b)

    r = calc(a, b)
    if a > b:
        assert r == 1
    elif a == b:
        assert r == 0
    else:
        assert r == -1


@pytest.mark.parametrize('a,b,c', [
    (0, 0, 1),
    (1, 0, 0),
    (0, 1, 0),
    (1, 1, 0),
])
def test_isnan(a, b, c):
    @ti.kernel
    def calc(a: ti.f32, b: ti.f32) -> ti.i32:
        return isnan(a / b)

    r = calc(a, b)
    assert r == c


@pytest.mark.parametrize('a,b,c', [
    (0, 0, 0),
    (1, 0, 1),
    (0, 1, 0),
    (1, 1, 0),
])
def test_isinf(a, b, c):
    @ti.kernel
    def calc(a: ti.f32, b: ti.f32) -> ti.i32:
        return isinf(a / b)

    r = calc(a, b)
    assert r == c
