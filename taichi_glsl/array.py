'''
(Experimental) Function aliases on Taichi tensor definitions.
'''

import taichi as ti
from typing import List, NewType


def dtype(dt):
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
    if dt in dt_map.keys():
        return dt_map[dt]
    else:
        return dt


DataType = NewType('DataType', (str, type))


def array(dt: DataType, *shape: List[int]):
    return ti.var(dt=dtype(dt), shape=shape)


# TODO: use array(Vec[n, dt], *shape) instead:
def vec_array(n: int, dt, *shape: List[int]):
    return ti.Vector(n, dt=dtype(dt), shape=shape)


def mat_array(n: int, m: int, dt: DataType, *shape: List[int]):
    return ti.Matrix(n, m, dt=dtype(dt), shape=shape)


def uniform(dt: DataType):
    return ti.var(dt=dtype(dt), shape=())


def vec_uniform(n: int, dt: DataType):
    return ti.Vector(n, dt=dtype(dt), shape=())


def mat_uniform(n: int, m: int, dt: DataType):
    return ti.Matrix(n, m, dt=dtype(dt), shape=())


def tensor(dt: DataType, shape: (List[int], None) = None):
    return ti.var(dt=dtype(dt), shape=shape)


def vec_tensor(n: int, dt: DataType, shape: (List[int], None) = None):
    return ti.Vector(n, dt=dtype(dt), shape=shape)


def mat_tensor(n: int, m: int, dt: DataType, shape: (List[int], None) = None):
    return ti.Matrix(n, m, dt=dtype(dt), shape=shape)
