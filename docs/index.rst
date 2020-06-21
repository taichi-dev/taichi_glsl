Taichi GLSL API references
==========================

Taichi GLSL is an extension library of the `Taichi Programming Language <https://github.com/taichi-dev/taichi>`_, which provides a set of useful helper functions including but not limited to:

1. Handy scalar functions like ``clamp``, ``smoothstep``, ``mix``, ``round``.
2. GLSL-alike vector functions like ``normalize``, ``distance``, ``reflect``.
3. Well-behaved random generators including ``randUnit3D``, ``randNDRange``.
4. Possible Taichi BUG hotfixes that are not yet released in it's cycle.
5. Handy vector and matrix initializer: ``vec`` and ``mat``.
6. Handy vector component shuffle accessor like ``v.xy``.


.. toctree::
   :maxdepth: 2
   :caption: Contents:


Scalar math
-----------

.. automodapi:: taichi_glsl.glsl

    :no-heading:

    :skip: acos, asin, ceil, cos, exp, floor, log, sin, sqrt, tan


Linear alegbra
--------------

.. automodapi:: taichi_glsl.linalg

    :no-heading:

Random generator
----------------

.. automodapi:: taichi_glsl.rand

    :no-heading:

Physics computation
-------------------

.. automodapi:: taichi_glsl.phys

    :no-heading:
