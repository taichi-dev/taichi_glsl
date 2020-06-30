'''
(Experimental) Some ODOP tools that might be useful in fluid dynamics simulation.
'''

import taichi as ti
import taichi_glsl as ts

from .field import *


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
