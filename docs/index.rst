Taichi GLSL API references
==========================

Taichi GLSL is an extension library of the `Taichi Programming Language <https://github.com/taichi-dev/taichi>`_, which provides a set of useful helper functions including but not limited to:

1. Handy scalar functions like ``clamp``, ``smoothstep``, ``mix``, ``round``.
2. GLSL-alike vector functions like ``normalize``, ``distance``, ``reflect``.
3. Well-behaved random generators including ``randUnit3D``, ``randNDRange``.
5. Handy vector and matrix initializer: ``vec`` and ``mat``.
6. Handy vector component shuffle accessor like ``v.xy``.
4. Handy field sampler including ``bilerp`` and ``sample``.
7. Useful physics helper functions like ``boundReflect``.
8. Shadertoy-alike inputed GUI base class ``Animation``.

Let me know if you encountered bugs or got a good idea by `opening an
issue on GitHub <https://github.com/taichi-dev/taichi_glsl/issues/new>`_.

.. note::

    Here's the documentation of **Taichi GLSL, the extension library**.
    For the documentation of **Taichi itself**, please click
    `here <https://taichi.readthedocs.io/en/stable>`_ |
    `这里 <https://taichi.readthedocs.io/zh_CN/stable>`_.

Installation
------------

To install, make sure you have installed ``taichi`` first, then install
``taichi_glsl`` via ``pip``:

.. code-block:: bash

    python3 -m pip install --user taichi_glsl

Import me using:

.. code-block:: python

    import taichi as ti
    import taichi_glsl as ts

Or simply:

.. code-block:: python

    from taichi_glsl import *

Note that this will import ``taichi`` as name ``ti`` as well.


Scalar math
-----------

.. automodapi:: taichi_glsl.scalar

    :no-heading:

    :skip: acos, asin, ceil, cos, exp, floor, log, sin, sqrt, tan

Vector math
-----------

.. automodapi:: taichi_glsl.vector

    :no-heading:

GUI Base Class
--------------

.. automodapi:: taichi_glsl.gui

    :no-heading:
    :no-inheritance-diagram:

Random generator
----------------

.. automodapi:: taichi_glsl.randgen

    :no-heading:

Field sampling
--------------

.. automodapi:: taichi_glsl.sampling

    :no-heading:

Particle simluation
-------------------

.. automodapi:: taichi_glsl.lagrangian

    :no-heading:

