import taichi as ti
import taichi_glsl as ts
import warnings
ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        res = 512, 512
        self.color = ts.Maccormack.make(lambda: ti.var(ti.f32, res))
        self.vel = ts.Maccormack.make(lambda: ti.Vector(2, ti.f32, res))
        self.img = self.color.new
        self.dt = 0.002
        self.dx = 1 / res[0]
        self.define_input()

    @ti.func
    def velocity(self, P):
        return ts.linearSample(self.vel.old, P)

    @ti.kernel
    def on_start(self):
        for I in ti.grouped(self.color):
            self.color.old[I] = 1 - ts.insideTaichi(I / self.iResolution)
        for P in ti.grouped(self.color):
            p = P * self.dx
            self.vel.old[P] = (2 * p - 1).yx * ts.vec(-1, 1)

    @ti.kernel
    def on_advance(self):
        self.color.advance(self)
        self.vel.advance(self)
        self.color.update()
        self.vel.update()


MyAnimation().start()
