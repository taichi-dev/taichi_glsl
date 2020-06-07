project_name = 'taichi_glsl'
version = '0.0.1'
description = 'Manipulate Taichi with GLSL-alike functions / APIs'
classifiers = [
    'Programming Lauguage :: Python :: 3',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Topic :: Multimedia :: Graphics',
    'Topic :: Games/Entertainment :: Simulation',
    'Operating System :: OS Independent',
]
python_requires = '>=3.6'
install_requires = [
    'numpy',
    'taichi>=0.6.7',
    # For testing:
    'pytest',
]
import setuptools

with open('README.md', 'r') as f:
  long_description = f.read()

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
