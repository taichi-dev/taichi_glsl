Taichi GLSL
===========

This package enables you to manipulate Taichi with GLSL-alike functions / APIs.


How to use
----------

First, import Taichi and Taichi GLSL:
```py
import taichi as ti
import taichi_glsl as ts
```

Or simply:
```py
from taichi_glsl import *
```


Then, in your Taichi kernels:
```py
@ti.kernel
def kern():
  v = vec(2.0, 3.0)
  v = ts.normalize(v)
  v = ts.clamp(v)
  print(v)
```
