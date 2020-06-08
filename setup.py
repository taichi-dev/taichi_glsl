project_name = 'taichi_glsl'
version = '0.0.1'
description = 'Manipulate Taichi with GLSL-alike helper functions'
long_description = '''
Taichi GLSL
===========

Taichi GLSL provides a set of helper functions, which enables you to manipulate the `Taichi Programming Language <https://github.com/taichi-dev/taichi>`_ in a GLSL-alike manner (work in progress).
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
    'taichi>=0.6.7',
]
with open('README.md', 'r') as f:
    long_description = f.read()

import setuptools

setuptools.setup(
    name=project_name,
    version=version,
    author='彭于斌',
    author_email='1931127624@qq.com',
    description=description,
    #long_description=long_description,
    classifiers=classifiers,
    python_requires=python_requires,
    install_requies=install_requires,
    packages=setuptools.find_packages(),
)
