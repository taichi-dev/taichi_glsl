'''
GLSL-alike scalar arithmetic functions.
'''

import taichi as ti
from taichi import sin, cos, tan, asin, acos, floor, ceil, sqrt, exp, log


@ti.func
def clamp(x, xmin=0, xmax=1):
    '''
    Constrain a value to lie between two further values.
    `clamp` returns the value of x constrained to the range xmin to xmax.

    :parameter x:
        Specify the value to constrain.
    :parameter xmin:
        Specify the lower end of the range into which to constrain x.
    :parameter xmax:
        Specify the upper end of the range into which to constrain x.

    :return:
        The returned value is computed as `min(xmax, max(xmin, x))`.
    '''
    return min(xmax, max(xmin, x))


@ti.func
def mix(x, y, a):
    '''
    Linearly interpolate between two values.

    `mix` performs a linear interpolation between x and y using a to
    weight between them.

    :parameter x:
        Specify the start of the range in which to interpolate.
    :parameter y:
        Specify the end of the range in which to interpolate.
    :parameter a:
        Specify the value to use to interpolate between x and y.

    :return:
        The return value is computed as `x * (1 - a) + y * a`.
    '''
    return x * (1 - a) + y * a


@ti.func
def sign(x, edge=0):
    '''
    Extract the sign of the parameter.

    `sign` returns -1.0 if x is less than edge, 0.0 if x is
    equal to edge, and +1.0 if x is greater than edge.

    :parameter x:
        Specify the value from which to extract the sign.
    :parameter edge:
        Specify a custom location of the edge instead of 0.

    :note:
        `sign(x, edge)` is equivalent with `sign(x - edge)`.

    :return:
        The return value is computed as `(x >= edge) - (x <= edge)`,
        with type promoted.
    '''
    ret = x + edge  # type promotion
    ret = (x >= edge) - (x <= edge)
    return ret


@ti.func
def step(edge, x):
    '''
    Generate a step function by comparing two values.

    `step` generates a step function by comparing x to edge.
    For element i of the return value, 0.0 is returned if x[i] < edge[i], and 1.0 is returned otherwise.

    :parameter edge:
        Specify the location of the edge of the step function.
    :parameter x:
        Specify the value to be used to generate the step function.

    :return:
        The return value is computed as `x >= edge`, with type
        promoted.
    '''
    ret = x + edge  # type promotion
    ret = (x >= edge)
    return ret


@ti.func
def atan(y, x=1):
    '''
    Return the arc-tangent of the parameters

    `atan(y, x)` or `atan(y_over_x)`:

    `atan` returns the angle whose trigonometric arctangent is y / x or
    y_over_x, depending on which overload is invoked.

    In the first overload, the signs of y and x are used to determine
    the quadrant that the angle lies in. The values returned by atan in
    this case are in the range [−pi, pi]. Results are undefined if x
    is zero.

    For the second overload, atan returns the angle whose tangent
    is y_over_x. Values returned in this case are in the range
    [−pi/2, pi/2].

    :parameter y:
        The numerator of the fraction whose arctangent to return.

    :parameter x:
        The denominator of the fraction whose arctangent to return.

    :return:
        The return value is `arctan(x / y)`.
    '''
    return ti.atan2(y, x)


@ti.func
def fract(x):
    '''
    Compute the fractional part of the argument.

    `fract` returns the fractional part of x.

    :parameter x:
        Specify the value to evaluate.

    :return:
        The return value is calculated as `x - floor(x)`.
    '''
    return x - floor(x)


@ti.func
def round(x):
    '''
    Find the nearest integer less than or equal to the parameter.

    `round` returns a value equal to the nearest integer to x.
    The fraction 0.5 will round toward the larger integer. i.e.
    `round(0.5) = 1.0`.

    :parameter x:
        Specify the value to evaluate.

    :return:
        The return value is calculated as `floor(x + 0.5)`.
    '''
    return floor(x + 0.5)


@ti.func
def smoothstep(x, a=0, b=1):
    '''
    Perform Hermite interpolation between two values.

    `smoothstep` performs smooth Hermite interpolation between 0 and 1
    when a < x < b. This is useful in cases where a threshold function
    with a smooth transition is desired.

    Results are undefined if a >= b.

    :parameter a:
        Specifies the value of the lower edge of the Hermite function.
    :parameter b:
        Specifies the value of the upper edge of the Hermite function.
    :parameter x:
        Specifies the source value for interpolation.

    :return:
        The return value is is computed as::
            t = clamp((x - a) / (b - a), 0, 1)
            return t * t * (3 - 2 * t)
    '''
    t = clamp((x - a) / (b - a))
    return t * t * (3 - 2 * t)


@ti.func
def inversesqrt(x):
    '''
    Return the inverse of the square root of the parameter.

    `inversesqrt` returns the inverse of the square root of x; i.e.
    the value `1 / sqrt(x)`. The result is undefined if x <= 0.

    :parameter x:
        Specify the value of which to take the inverse of the square root.

    :return:
        The return value can be calculated as `1 / sqrt(x)` or `pow(x, -0.5)`.
    '''
    return 1 / ti.sqrt(x)


@ti.func
def isnan(x):
    '''
    Determine whether the parameter is a number.

    For each element element i of the result, `isnan` returns True
    if x[i] is posititve or negative floating point NaN (Not a Number)
    and False otherwise.

    :parameter x:
        Specifies the value to test for NaN.

    :return:
        The return value is computed as `not (x >= 0 or x <= 0)`.
    '''
    return not (x >= 0 or x <= 0)


@ti.func
def isinf(x):
    '''
    Determine whether the parameter is positive or negative infinity.

    For each element element i of the result, `isinf` returns True
    if x[i] is posititve or negative floating point infinity and
    False otherwise.

    :parameter x:
        Specifies the value to test for infinity.

    :return:
        The return value is computed as `2 * x == x and x != 0`.
    '''
    return 2 * x == x and x != 0
