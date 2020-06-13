'''
Manipulate Taichi with GLSL-alike helper functions.
'''

import taichi as ti
import numpy as np

from .version import version as __version__
print(f'[TaiGLSL] version {__version__}')

from .glsl import *
from .array import *
from .linalg import *
from .transform import *
import math
