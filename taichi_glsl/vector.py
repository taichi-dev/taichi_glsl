'''
GLSL-alike linear algebra helper functions / aliases.
'''

import taichi as ti


def vecSimple(*xs):
    '''
    Create a n-D vector whose components are specified by arguments.

    :parameter xs:
        Specify the scalar values to initialize the vector components.

    :return:
        The return value is a n-D vector, where `n = len(xs)`.
        And the i-th component is initialized to be `xs[i]`.

    :see also:
        :func:`vec`, :func:`vecFill`.
    '''
    return ti.Vector(xs)


def vec(*xs):
    '''
    Create a vector by scalars or vectors in arguments (GLSL-alike).

    The return vector dimension depends on **the count of scalars in xs**.

    :parameter xs:
        Specify the scalar or vector values to initialize the
        vector components. If xs[i] is vector, it will be **flatten**
        into a series of scalars.

    :return:
        A n-D vector initialized as described above.

    :see also:
        :func:`vecND`, :func:`vecSimple`, :func:`vecFill`.
    '''
    ys = []
    for x in xs:
        if isinstance(x, ti.Matrix):
            ys.extend(x.entries)
        else:
            ys.append(x)
    return vecSimple(*ys)


def vecND(n, *xs):
    '''
    Create a n-D vector by scalars or vectors in arguments (GLSL-alike).

    The return vector dimension depends on **the specified argument n**.
    If the dimension mismatch the count of scalars in xs, an error
    will be raised.
    However, if only one scalar is specified, then `vecND(n, x)` is
    equivalent to `vecFill(n, x)`, see :func:`vecFill`.

    :parameter n:
        Specify the dimension of return vector.
    :parameter xs:
        Specify the scalar or vector values to initialize the
        vector components. If xs[i] is vector, it will be **flatten**
        into a series of scalars.

    :return:
        A n-D vector initialized as described above.

    :note:
        `vecND(n, x)` -> `vecFill(n, x)`
        `vecND(n, x, y, ...)` -> `vec(x, y, ...)`

    :see also:
        :func:`vec`, :func:`vec2`, :func:`vec3`.
    '''
    # This's not inside of `@ti.func`, so it's safe to multi-return.
    # The `if` statement here is branched at compile-time.
    if len(xs) == 1 and not isinstance(xs[0], ti.Matrix):
        return vecFill(n, xs[0])

    ys = []
    for x in xs:
        if isinstance(x, ti.Matrix):
            ys.extend(x.entries)
        else:
            ys.append(x)

    if len(ys) != n:
        raise ValueError(f'Cannot generate {n}-D vector from '
                         f'{len(ys)} scalars')

    return vecSimple(*ys)


def vecFill(n, x):
    '''
    Create a n-D vector whose all components are initialized by x.

    :parameter x:
        Specify the scalar value to fill the vector.

    :return:
        The return value is calculated as `vec(x for _ in range(n))`.

    :see also:
        :func:`vecND`, :func:`vec`, :func:`vec3`.
    '''
    return ti.Vector([x for _ in range(n)])


def vec2(*xs):
    '''
    An alias for `vecND(2, *xs)`.

    :see also:
        :func:`vecND`, :func:`vec`, :func:`vec3`.
    '''
    return vecND(2, *xs)


def vec3(*xs):
    '''
    An alias for `vecND(3, *xs)`.

    :see also:
        :func:`vecND`, :func:`vec`, :func:`vec2`.
    '''
    return vecND(3, *xs)


def vec4(*xs):
    '''
    An alias for `vecND(4, *xs)`.

    :see also:
        :func:`vecND`, :func:`vec`, :func:`vec3`.
    '''
    return vecND(4, *xs)


def vecAngle(a):
    '''
    Return a 2D vector of specific phase angle.

    :parameter a:
        Specify the phase angle of vector.

    :return:
        The return value is computed as `vec(cos(a), sin(a))`.
    '''
    return vecSimple(ti.cos(a), ti.sin(a))


def mat(*xs):
    '''
    Matrix initializer (WIP).

    :parameter xs:
        A row-major list of list, which contains the elements of matrix.

    :return:
        A matrix, size depends on the input xs.

    For example::
        mat([1, 2], [3, 4])

    (TODO: WIP)
    '''
    return ti.Matrix(xs)


def dot(a, b):
    '''
    Calculate the dot product of two vectors.

    `dot` returns the dot product of two vectors, i.e.,
    `x[0] * y[0] + x[1] * y[1] + ...`.

    :parameter x:
        Specifies the first of two vectors.
    :parameter y:
        Specifies the second of two vectors.

    :return:
        The return value can be calculated as `summation(a * b)`.

    :see also:
        :func:`cross`, :func:`length`, :func:`outerProduct`,
        :func:`summation`.
    '''
    return a.dot(b)


def normalize(v):
    '''
    Calculates the unit vector in the same direction as the original vector.

    `normalize` returns a vector with the same direction as its parameter,
    `v`, but with length 1.

    :parameter v:
        Specifies the vector to normalize.

    :return:
        The return value can be calculated as `v * invLength(v)`.

    :see also:
        :func:`dot`, :func:`length`, :func:`invLength`.
    '''
    return v.normalized()


@ti.func
def normalizePow(v, n, eps=0):
    '''
    Return a vector with same direction but with a `n`-powered length.

    This can be used in calculating gravitational force or speed around vortex.

    :parameter v:
        Specifies the vector to normalize.

    :parameter n:
        Specifies the power number to tweak the length.

    :return:
        The return value can be calculated as `normalize(v) * length(v) ** n`.
    '''
    l2 = v.norm_sqr() + eps
    return v * (l2**((n - 1) / 2))


def summation(v):
    '''
    Calculate the sum of all elements in a vector.

    `summation` returns the sum of vector elements, i.e.,
    `v[0] + v[1] + ...`.

    :parameter v:
        Specifies the vector whose elements to sum up.

    :return:
        The return value is the sum of all elements in `v`.

    :see also:
        :func:`minimum`, :func:`maximum`.
    '''
    return v.sum()


def maximum(v):
    '''
    Find the maximum value in all elements of a vector.

    `maximum` returns the maximum value in vector elements, i.e.,
    `max(v[0], v[1] + ...)`.

    :parameter v:
        Specifies the vector where to find the maximum element.

    :return:
        The return value is the maximum value in vector elements.

    :see also:
        :func:`minimum`, :func:`summation`.
    '''
    return v.max()


def minimum(v):
    '''
    Find the minimum value in all elements of a vector.

    `minimum` returns the minimum value in vector elements, i.e.,
    `max(v[0], v[1] + ...)`.

    :parameter v:
        Specifies the vector where to find the minimum element.

    :return:
        The return value is the minimum value in vector elements.

    :see also:
        :func:`maximum`, :func:`summation`.
    '''
    return v.min()


def cross(a, b):
    '''
    Calculate the cross product of two vectors.
    The argument can be 2D or 3D. If 3D, the return value is 3D;
    If 2D, the return value is a scalar.
    The computation is done in a right-handed coordinate system, i.e.::

        cross(vec(1, 0, 0), vec(0, 1, 0)) == vec(0, 0, 1)
        cross(vec(1, 0), vec(0, 1)) == 1

    :parameter x:
        Specifies the first of two vectors, can be 2D or 3D.
    :parameter y:
        Specifies the second of two vectors, can be 2D or 3D.

    :return:
        The return value can be calculated as `summation(a * b)`.

    For example::

        a = vec(1, 2, 3)
        b = vec(4, 5, 6)
        c = cross(a, b)
        # c = [2*6 - 5*3, 4*3 - 1*6, 1*5 - 4*2] = [-3, 6, -3]

        p = vec(1, 2)
        q = vec(4, 5)
        r = cross(a, b)
        # r = 1*5 - 4*2 = -3
    '''
    return a.cross(b)


def outerProduct(a, b):
    return a.outer_product(b)


def sqrLength(x):
    '''
    Calculate the square of the length of a vector.

    `sqrLength` returns the square of length of the vector, i.e.,
    `x[0] ** 2 + x[1] * 2 + ...`.

    :parameter x:
        Specifies a vector of which to calculate the length.

    :return:
        The return value can be calculated as `dot(x, x)`.

    :see also:
        :func:`length`, :func:`dot`, :func:`invLength`.
    '''
    return x.norm_sqr()


def length(x):
    '''
    Calculate the length of a vector.

    `length` returns the length or magnitude of the vector, i.e.,
    `sqrt(x[0] ** 2 + x[1] * 2 + ...)`.

    :parameter x:
        Specifies a vector of which to calculate the length.

    :return:
        The return value can be calculated as `sqrt(dot(x, x))`.

    :see also:
        :func:`distance`, :func:`invLength`, :func:`dot`.
    '''
    return x.norm()


def invLength(x):
    '''
    Calculate the inverse of length of a vector.

    `invLength` returns the inverse of the magnitude of the vector, i.e.,
    `1 / sqrt(x[0] ** 2 + x[1] * 2 + ...)`.

    :parameter x:
        Specifies a vector of which to calculate the length.

    :return:
        The return value can be calculated as `inversesqrt(dot(x, x))`.

    :see also:
        :func:`length`, :func:`normalize`, :func:`inversesqrt`.
    '''
    try:
        return x.norm_inv()
    except:
        return 1 / x.norm()


@ti.func
def distance(a, b):
    '''
    Calculate the distance between two points.

    :parameter a:
        Specifies the first of two points.

    :parameter b:
        Specifies the second of two points.

    :return:
        The return value is calculated as `length(a - b)`.

    :see also:
        :func:`length`, :func:`normalize`, :func:`dot`.
    '''
    return (a - b).norm()


@ti.func
def reflect(I, N):
    '''
    Calculate the reflection direction for an incident vector.

    :parameter I:
        Specifies the incident vector.
    :parameter N:
        Specifies the normal vector.

    :return:
        For a given incident vector I and surface normal N, `reflect`
        returns the reflection direction calculated as
        `I - 2 * dot(N, I) * N`.

    :note:
        N should be normalized in order to achieve the desired result.

    :see also:
        :func:`refract`, :func:`normalize`, :func:`dot`.
    '''
    return I - 2 * dot(N, I) * N


@ti.func
def refract(I, N, eta):
    '''
    Calculate the refraction direction for an incident vector.

    For a given incident vector I, surface normal N and ratio of indices
    of refraction, eta, refract returns the refraction vector, R.

    :parameter I:
        Specifies the incident vector.
    :parameter N:
        Specifies the normal vector.
    :parameter eta:
        Specifies the ratio of indices of refraction.

    :return:
        The return value is calculated as::

            k = 1 - eta * eta * (1 - dot(N, I) * dot(N, I))
            R = I * 0
            if k >= 0:
                R = eta * I - (eta * dot(N, I) + sqrt(k)) * N
            return R

    :note:
        The input parameters I and N should be normalized in order to
        achieve the desired result.

    :see also:
        :func:`reflect`, :func:`normalize`, :func:`dot`.
    '''
    NoI = dot(N, I)
    k = 1 - eta**2 * (1 - NoI**2)
    R = I * 0
    if k >= 0:
        R = eta * I - (eta * NoI + ti.sqrt(k)) * N


def shuffle(a, *ks):
    ret = []
    for k in ks:
        t = a.subscript(k)
        ret.append(ti.expr_init(t))
    return ti.Vector(ret)


def _vector_getattr(self, key):
    ret = []
    stk = []
    for k in key:
        sgn = 0
        i = 0
        if k != '_':
            sgn = 1
            i = 'xyzw'.find(k)
            if i == -1:
                sgn = -1
                i = 'XYZW'.find(k)
                if i == -1:
                    break

        stk.append((i, sgn))

    else:
        for i, sgn in stk:
            if ti.inside_kernel():
                t = self.subscript(i) * sgn
                ret.append(ti.expr_init(t))
            else:
                t = self[i] * sgn
                ret.append(t)

        return ti.Vector(ret)

    _taichi_skip_traceback = 1
    raise AttributeError(f"'Matrix' object has no attribute {key}")


ti.Matrix.__getattr__ = _vector_getattr
