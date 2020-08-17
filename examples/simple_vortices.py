import taichi as ti

import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        res = 512, 512
        self.color = ts.Maccormack.make(lambda: ti.var(ti.f32, res))
        self.vorts = ti.Vector(2, ti.f32, 4)
        self.circles = self.vorts
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
            dis = dis.yx * ts.vec(1, -1)
            vel += dis
        return vel * 0.01

    @ti.kernel
    def on_start(self):
        for I in ti.grouped(self.color):
            p = I / self.iResolution
            self.color.old[I] = ts.imageGrid(p)
        self.vorts[0] = ts.vec(0.25, 0.5)
        self.vorts[1] = ts.vec(0.75, 0.5)
        self.vorts[2] = ts.vec(0.5, 0.25)
        self.vorts[3] = ts.vec(0.5, 0.75)

    @ti.kernel
    def on_advance(self):
        self.color.advance(self)
        self.color.update()


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
