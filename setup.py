project_name = 'taichi_glsl'
from taichi_glsl.version import version, taichi_version
description = 'A Taichi extension library providing a set of GLSL-alike helper functions'
long_description = '''
Taichi GLSL
===========

Taichi GLSL is an extension library of the `Taichi Programming Language <https://github.com/taichi-dev/taichi>`_, which provides a set of useful helper functions including but not limited to:

1. Handy scalar functions like ``clamp``, ``smoothstep``, ``mix``, ``round``.
2. GLSL-alike vector functions like ``normalize``, ``distance``, ``reflect``.
3. Well-behaved random generators including ``randUnit2D``, ``randNDRange``.
4. Possible Taichi BUG hotfixes that are not yet released in it's cycle.
5. Handy vector and matrix initializer: ``vec`` and ``mat``.
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
    install_requies=install_requires,
    packages=setuptools.find_packages(),
)
