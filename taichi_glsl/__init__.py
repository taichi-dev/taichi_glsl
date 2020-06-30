'''
Manipulate Taichi with GLSL-alike helper functions.
'''

import taichi as ti
import numpy as np
import math

from .version import version as __version__
from .hack import *
from .scalar import *
from .vector import *
from .odop import *
from .randgen import *
from .sampling import *
from .lagrangian import *
from .experimental.array import *
from .experimental.transform import *
from .experimental.cfd import *
from .mkimages import *
from .colormap import *
from .gui import *
