import taichi as ti
import numpy as np


### Shader Functions ###

from taichi import sin, cos, tan, asin, acos, floor, ceil, sqrt

def vec(*xs):
  return ti.Vector(xs)

def mat(*xs):
  return ti.Matrix(xs)

@ti.func
def clamp(x, xmin=0, xmax=1):
  return min(xmax, max(xmin, x))

@ti.func
def mix(a, b, t):
  return a * t + (b - a) * t

@ti.func
def step(x):
  return (x >= 0) - (x <= 0)

@ti.func
def normalize(x):
  return x.normalized()

@ti.func
def dot(a, b):
  return a.dot(b)

@ti.func
def cross(a, b):
  return a.cross(b)

@ti.func
def outerProduct(a, b):
  return a.outer_product(b)

@ti.func
def length(x):
  return x.norm()

@ti.func
def distance(a, b):
  return (a - b).norm()

@ti.taichi_scope
def shuffle(a, *indices):
  ret = []
  for i in indices:
    t = a.subscript(i)
    ret.append(t)
  return ti.Vector(ret)

@ti.func
def atan(a, b=1):
  return ti.atan2(a, b)

@ti.func
def fract(x):
  return x - x % 1

@ti.func
def round(x):
  return int(x + 0.5)

@ti.func
def smoothstep(x, a=0, b=1):
  t = clamp((x - a) / (b - a))
  return t * t * (3 - 2 * t)


### Array Definitions ###

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


### Transforms ###

def _tuple_to_vector(x):
  if len(x) != 1 or not isinstance(x[0], Matrix):
    x = ti.Matrix(x)
  return x

def view(image, *indices):
  indices = _tuple_to_vector(indices)
  return indices / image.shape()

def tex(image, *coors):
  coors = _tuple_to_vector(coors)
  return indices / image.shape()


### Pre-init ###

ti.init()
