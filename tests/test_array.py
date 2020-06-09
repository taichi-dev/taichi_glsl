from taichi_glsl import *
import pytest

dt_map = {
    'float32': ti.f32,
    'float64': ti.f64,
    'int8': ti.i8,
    'int16': ti.i16,
    'int32': ti.i32,
    'int64': ti.i64,
    'uint8': ti.u8,
    'uint16': ti.u16,
    'uint32': ti.u32,
    'uint64': ti.u64,
    'float': ti.f32,
    'int': ti.i32,
    float: ti.f32,
    int: ti.i32,
}

shapes = [(), (2, ), (3, 4)]


@pytest.mark.parametrize('dt_name,dt', dt_map.items())
def test_dtype(dt_name, dt):
    assert dtype(dt_name) == dt


@pytest.mark.parametrize('shape', shapes)
@pytest.mark.parametrize('dt', set(dt_map.values()))
@ti.host_arch_only
def test_array(dt, shape):
    x = array(dt, *shape)

    @ti.kernel
    def func0():
        x[None] = 2

    @ti.kernel
    def func1():
        for i in x:
            x[i] = i + 1

    @ti.kernel
    def func2():
        for i, j in x:
            x[i, j] = i + j + 1

    eval(f'func{len(shape)}')()


@pytest.mark.parametrize('dt', [float, int])
@ti.host_arch_only
def test_mat_array(dt):
    x = mat_array(2, 3, dt, 4, 3)

    @ti.kernel
    def func():
        for i, j in x:
            x[i, j] = mat([2, 3, 4], [5, 6, 7])

    func()


@pytest.mark.parametrize('dt', [float, int])
@ti.host_arch_only
def test_vec_array(dt):
    x = vec_array(3, dt, 2, 3)

    @ti.kernel
    def func():
        for i, j in x:
            x[i, j] = vec(2, 3, 4)

    func()
