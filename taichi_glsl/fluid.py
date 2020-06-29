'''
Some ODOP tools that might be useful in fluid dynamics simulation.
'''


import taichi as ti
import taichi_glsl as ts

from .odop import TaichiClass


@ti.func
def clampSample(field: ti.template(), P):
    shape = ti.Vector(field.shape())
    P = ts.clamp(P, 1, shape - 1)
    return field[P]


@ti.func
def linearSample(field: ti.template(), P):
    I = int(P)
    x = ts.fract(P)
    y = 1 - x
    D = ts.vec(1, 0)
    return (clampSample(field, I + D.xx) * x.x * x.y +
            clampSample(field, I + D.xy) * x.x * y.y +
            clampSample(field, I + D.yy) * y.x * y.y +
            clampSample(field, I + D.yx) * y.x * x.y)



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


class SemiLagrangianRK2(SemiLagrangianRK1):
    @ti.func
    def advance(self, world):
        for I in ti.grouped(self.old):
            spI = I - world.velocity(I) * (0.5 * world.dt / world.dx)
            btI = I - world.velocity(spI) * (world.dt / world.dx)
            self.new[I] = linearSample(self.old, btI)


class Maccormack(Pair):
    @classmethod
    def make(cls, init, base=SemiLagrangianRK2):
        a, b, c = init(), init(), init()
        ret = cls(a, b, c)
        ret.forth, ret.back = base(a, b), base(b, c)
        return ret

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
