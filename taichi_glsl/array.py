import taichi as ti


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
        'double': ti.f64,
        'char': ti.i8,
        'short': ti.i16,
        'int': ti.i32,
        'int64_t': ti.i64,
        'uchar': ti.u8,
        'ushort': ti.u16,
        'uint': ti.u32,
        'uint64_t': ti.u64,
        float: ti.f32,
        int: ti.i32,
    }
    if dt in dt_map.keys():
        return dt_map[dt]
    else:
        return dt


def array(dt, *shape):
    return ti.var(dtype(dt), shape)


def vec_array(n, dt, *shape):
    return ti.Vector(n, dtype(dt), shape)


def mat_array(n, m, dt, *shape):
    return ti.Matrix(n, m, dtype(dt), shape)


def uniform(dt):
    return ti.var(dtype(dt), ())


def vec_uniform(n, dt):
    return ti.Vector(n, dtype(dt), ())


def mat_uniform(n, m, dt):
    return ti.Matrix(n, m, dtype(dt), ())
