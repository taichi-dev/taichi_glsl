project_name = 'taichi_glsl'
from taichi_glsl.version import version, taichi_version
version = '.'.join(map(str, version))
taichi_version = '.'.join(map(str, taichi_version))
description = 'A Taichi extension library providing a set of GLSL-alike helper functions'
long_description = '''
Taichi GLSL
===========

Taichi GLSL is an extension library of the `Taichi Programming Language <https://github.com/taichi-dev/taichi>`_, which provides a set of useful helper functions including but not limited to:

1. Handy scalar functions like ``clamp``, ``smoothstep``, ``mix``, ``round``.
2. GLSL-alike vector functions like ``normalize``, ``distance``, ``reflect``.
3. Well-behaved random generators including ``randUnit3D``, ``randNDRange``.
4. Handy vector and matrix initializer: ``vec`` and ``mat``.
5. Handy vector component shuffle accessor like ``v.xy``.
6. Handy field sampler including ``bilerp`` and ``sample``.
7. Useful physics helper functions like ``boundReflect``.
8. Shadertoy-alike inputed GUI base class ``Animation``.

<[Clike me for documentation] (https://taichi-glsl.readthedocs.io)>_
<[Clike me for GitHub repo] (https://github.com/taichi-dev/taichi_glsl)>_
'''
classifiers = [
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Games/Entertainment :: Simulation',
    'Operating System :: OS Independent',
]
python_requires = '>=3.6'
install_requires = [
    'taichi>=' + taichi_version,
]

import setuptools

setuptools.setup(
    name=project_name,
    version=version,
    author='彭于斌',
    author_email='1931127624@qq.com',
    description=description,
    long_description=long_description,
    classifiers=classifiers,
    python_requires=python_requires,
    install_requires=install_requires,
    packages=setuptools.find_packages(),
)
