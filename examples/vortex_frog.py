import taichi as ti
import taichi_glsl as ts
import warnings
ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        res = 512, 512
        self.color = ts.Maccormack.make(lambda: ti.var(ti.f32, res))
        self.vorts = ti.Vector(2, ti.f32, 4)
        self.vorty = ti.var(ti.f32, 4)
        self.circles = self.vorts
        self.circle_radius = 3
        self.circle_color = 0x000000
        self.img = self.color.new
        self.dt = 0.04
        self.dx = 1 / res[0]
        self.define_input()

    @ti.func
    def velocity(self, P):
        p = P * self.dx
        vel = ts.vec2(0.0)
        for v in range(self.vorts.shape[0]):
            dis = (p - self.vorts[v])
            dis = ts.normalizePow(dis, -1, 0.001)
            dis = dis.yx * ts.vec(-1, 1) * self.vorty[v]
            vel += dis
        return vel * 0.01

    @ti.kernel
    def on_start(self):
        for I in ti.grouped(self.color):
            p = I / self.iResolution
            self.color.old[I] = ts.imageChess(p)
        self.vorts[0] = ts.vec(0.25, 0.25)
        self.vorts[1] = ts.vec(0.25, 0.40)
        self.vorts[2] = ts.vec(0.25, 0.60)
        self.vorts[3] = ts.vec(0.25, 0.75)
        self.vorty[0] = -1.0
        self.vorty[1] = -1.0
        self.vorty[2] = +1.0
        self.vorty[3] = +1.0

    @ti.kernel
    def on_advance(self):
        for v in self.vorts:
            vel = self.velocity(self.vorts[v] / self.dx)
            self.vorts[v] += vel * self.dt
        self.color.advance(self)
        self.color.update()


MyAnimation().start()
