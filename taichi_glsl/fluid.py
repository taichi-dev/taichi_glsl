'''
Some ODOP tools that might be useful in fluid dynamics simulation.
'''


import taichi as ti
import taichi_glsl as ts

from .odop import TaichiClass


D = ts.vec(1, 0, -1)


@ti.func
def clampSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    P = ts.clamp(P, 0, shape - 1)
    return field[P]


@ti.func
def blackSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    ret = field[P] * 0
    if all(0 <= P and P < shape):
        ret = field[P]
    return ret


@ti.func
def whiteSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    ret = field[P] * 0 + 1
    if all(0 <= P and P < shape):
        ret = field[P]
    return ret


@ti.func
def linearSample(field: ti.template(), P):
    I = int(P)
    x = ts.fract(P)
    y = 1 - x
    return (clampSample(field, I + D.xx) * x.x * x.y +
            clampSample(field, I + D.xy) * x.x * y.y +
            clampSample(field, I + D.yy) * y.x * y.y +
            clampSample(field, I + D.yx) * y.x * x.y)


@ti.func
def vgridDivergence(field: ti.template(), I):
    return ( clampSample(field, I + D.xy).x
           + clampSample(field, I + D.yx).y
           - clampSample(field, I + D.xz).x
           - clampSample(field, I + D.zx).y)


@ti.func
def vgridGradient(field: ti.template(), I):
    return ts.vec2(
            clampSample(field, I + D.yx) - clampSample(field, I + D.zx),
            clampSample(field, I + D.xy) - clampSample(field, I + D.xz))


@ti.func
def vgridSumAround(field: ti.template(), I):
    return ( clampSample(field, I + D.yx) + clampSample(field, I + D.zx)
           + clampSample(field, I + D.xy) + clampSample(field, I + D.xz))


class Pair(TaichiClass):
    @classmethod
    def make(cls, init):
        return cls(init(), init())

    @property
    def old(self):
        return self.entries[0]

    @property
    def new(self):
        return self.entries[1]

    @ti.func
    def update(self):
        for I in ti.grouped(self.old):
            self.old[I] = self.new[I]


class SemiLagrangianRK1(Pair):
    @ti.func
    def advance(self, world):
        for I in ti.grouped(self.old):
            btI = I - world.velocity(I) * (world.dt / world.dx)
            self.new[I] = linearSample(self.old, btI)


class SemiLagrangianRK2(Pair):
    @ti.func
    def advance(self, world):
        for I in ti.grouped(self.old):
            spI = I - world.velocity(I) * (0.5 * world.dt / world.dx)
            btI = I - world.velocity(spI) * (world.dt / world.dx)
            self.new[I] = linearSample(self.old, btI)


class Maccormack(Pair):
    def __init__(self, a, b, c, base=None):
        base = base or SemiLagrangianRK2
        super(Maccormack, self).__init__(a, b, c)
        self.forth, self.back = base(a, b), base(b, c)

    @classmethod
    def make(cls, init, base=None):
        a, b, c = init(), init(), init()
        return cls(a, b, c, base)

    @property
    def aux(self):
        return self.entries[2]

    @ti.func
    def advance(self, world):
        self.forth.advance(world)
        world.dt = ti.static(-world.dt)
        self.back.advance(world)
        world.dt = ti.static(-world.dt)

        for I in ti.grouped(self.old):
            self.new[I] += 0.5 * (self.old[I] - self.aux[I])
