Taichi GLSL
===========

Taichi GLSL provides a set of helper functions, which enables you to manipulate the [Taichi Programming Language](https://github.com/taichi-dev/taichi) in a GLSL-alike manner (work in progress).

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/taichi-dev/taichi_glsl/Persubmit%20Checks)

Installation
------------

Install Taichi and Taichi GLSL with `pip`:

```bash
# Python 3.6/3.7/3.8 (64-bit)
pip install taichi taichi_glsl
```


How to play
-----------

First, import Taichi and Taichi GLSL:
```py
import taichi as ti
import taichi_glsl as ts
```

---

Then, use `ts.xxx` helper functions in your Taichi kernels like this:
```py
@ti.kernel
def kern():
  a = ts.vec(2.2, -3.3)   # deduced to be vec2
  b = ts.normalize(a)     # get normalized vector
  c = ts.clamp(a)         # element-wise, clamp to range [0, 1]
  d = int(a)              # cast to ivec2, vector of integers
  print(b, c, d)          # [0.554700, -0.832050] [1.000000, 0.000000] [2, -3]
```

For Taichi documentations, click [here](https://taichi.readthedocs.io/en/stable) | [这里](https://taichi.readthedocs.io/zh_CN/stable)。

Hints
-----

If you don't like the `ts.` prefix, import using:

```py
from taichi_glsl import *

@ti.kernel
def kern():
  a = vec(2.33, 6.66)
  b = normalize(a)
  ...
```

Note that this will import `taichi` as name `ti` as well.

---

`vec2`, `vec3` and `vec4` are simply `vec` in Taichi GLSL:

```py
v = vec(2.0, 3.0)            # vec2
v = vec(2.0, 3.0, 4.0)       # vec3
v = vec(2.0, 3.0, 4.0, 5.0)  # vec4
v = vec(2, 3)                # ivec2 (since 2 is an integer)
```

Thanks to the python syntax of `vec(*args)`.

Example
-------

The following codes shows up an red-green UV map in the window:

```py
from taichi_glsl import *

image = vec_array(3, float, 512, 512)

@shader
def paint(img, coor):
    img[coor] = vec(coor.x, coor.y, 0.0)


paint(image)
ti.imshow(image)
```

Check out more examples in the `examples/` folder.
