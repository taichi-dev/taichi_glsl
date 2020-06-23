Taichi GLSL
===========

Taichi GLSL is an extension library of the [Taichi Programming Language](https://github.com/taichi-dev/taichi), which provides a set of useful helper functions including but not limited to:

1. Handy scalar functions like ``clamp``, ``smoothstep``, ``mix``, ``round``.
2. GLSL-alike vector functions like ``normalize``, ``distance``, ``reflect``.
3. Well-behaved random generators including ``randUnit3D``, ``randNDRange``.
4. Possible Taichi BUG hotfixes that are not yet released in it's cycle.
5. Handy vector and matrix initializer: ``vec`` and ``mat``.
6. Handy vector component shuffle accessor like ``v.xy``.

[[Clike me for documentation]](https://taichi-glsl.readthedocs.io)

[![Build Status](https://img.shields.io/github/workflow/status/taichi-dev/taichi_glsl/Persubmit%20Checks)](https://github.com/taichi-dev/taichi_glsl/actions?query=workflow%3A%22Persubmit+Checks%22)
[![Documentation Status](https://readthedocs.org/projects/taichi-glsl/badge?version=latest)](https://taichi-glsl.readthedocs.io/en/latest)
[![Coverage Status](https://img.shields.io/codecov/c/github/taichi-dev/taichi_glsl)](https://codecov.io/gh/taichi-dev/taichi_glsl)
[![Downloads](https://pepy.tech/badge/taichi-glsl/month)](https://pepy.tech/project/taichi-glsl/month)
[![Latest Release](https://img.shields.io/github/v/release/taichi-dev/taichi_glsl)](https://github.com/taichi-dev/taichi_glsl/releases)


Links
-----

[Taichi Main Repo](https://github.com/taichi-dev/taichi)
[Taichi THREE / Tai3D](https://github.com/taichi-dev/taichi_three)
[Taichi Documentation](https://taichi.readthedocs.io/en/stable)
[Taichi 中文文档](https://taichi.readthedocs.io/zh_CN/stable)
[Taichi GLSL Documentation](https://taichi-glsl.readthedocs.io)
[Forum Thread of Taichi GLSL](https://taichi-glsl.readthedocs.io)


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

@ti.kernel
def paint():
    for i, j in image:
        coor = view(image, i, j)
        image[i, j] = vec(coor.x, coor.y, 0.0)


paint()
ti.imshow(image)
```

Check out more examples in the `examples/` folder.
