import taichi as ti
import taichi_glsl as ts


@ti.func
def grayscale(rgb):
    '''
    Convert RGB value (vector) into grayscale (scalar).

    :parameter rgb: (3D vector)
        The RGB value, X compoment is the R value, can be eitier float or int.

    :return:
        The return value is calculated as `dot(vec(0.2989, 0.587, 0.114), rgb)`.
    '''
    ret = rgb.x
    ret = ts.vec(0.2989, 0.587, 0.114).dot(rgb)
    return ret


@ti.pyfunc
def normalmap(n):
    '''
    Convert XYZ normal vector into RGB values.

    :parameter n: (3D vector)
        The XYZ normal vector, should be normalized to get the desired output.

    :return:
        The return value is calculated as `n * 0.5 + 0.5`.
    '''
    return n * 0.5 + 0.5


@ti.func
def blueorange(rgb):
    '''
    Convert RGB value (vector) into blue-orange colormap (vector).

    :parameter rgb: (3D vector)
        The RGB value, X compoment is the R value, can be eitier float or int.

    :return:
        The return value is calculated as `sqrt(mix(vec(0, 0.01, 0.05), vec(1.19, 1.04, 0.98), color))`.
    '''
    blue = ts.vec(0.00, 0.01, 0.05)
    orange = ts.vec(1.19, 1.04, 0.98)
    return ti.sqrt(ts.mix(blue, orange, rgb))
