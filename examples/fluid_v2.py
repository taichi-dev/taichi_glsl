import taichi as ti
import taichi_glsl as ts
import warnings
ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        res = 512, 512
        self.color = ts.Maccormack.make(lambda: ti.var(ti.f32, res))
        self.vel = ts.Maccormack.make(lambda: ti.Vector(2, ti.f32, res))
        self.pre = ts.Pair.make(lambda: ti.var(ti.f32, res))
        self.div = ti.var(ti.f32, res)
        self.img = self.color.new
        self.dt = 0.004
        self.dx = 1 / res[0]
        self.define_input()

    @ti.func
    def velocity(self, P):
        return ts.linearSample(self.vel.old, P)

    @ti.func
    def clearDiv(self):
        for I in ti.grouped(ti.ndrange(*self.pre.old.shape)):
            self.div[I] = ts.vgridDivergence(self.vel.new, I)
        for _ in ti.static(range(5)):
            for I in ti.grouped(ti.ndrange(*self.pre.old.shape)):
                pa = ts.vgridSumAround(self.pre.old, I)
                self.pre.new[I] = (pa - self.div[I] * self.dx ** 2) * 0.25
            self.pre.update()
            for I in ti.grouped(ti.ndrange(*self.pre.old.shape)):
                grad = ts.vgridGradient(self.div, I) / self.dx
                self.vel.new[I] -= grad * self.dt * 0.03

    @ti.kernel
    def on_start(self):
        for I in ti.grouped(self.color):
            self.color.old[I] = ts.imageChess(I / self.iResolution)
        for P in ti.grouped(self.color):
            p = P * self.dx
            self.vel.old[P] = (2 * p - 1).yx * ts.vec(-1, 1)

    @ti.kernel
    def on_advance(self):
        self.vel.advance(self)
        self.color.advance(self)
        self.vel.update()
        self.color.update()
        for i in ti.static(range(5)):
            self.clearDiv()


MyAnimation().start()
