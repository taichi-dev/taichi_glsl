import taichi as ti

import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        res = 512, 512
        self.color = ts.Maccormack.make(lambda: ti.var(ti.f32, res))
        self.img = self.color.new
        self.dt = 0.04
        self.dx = 1 / res[0]
        self.define_input()

    @ti.func
    def velocity(self, P):
        p = P * self.dx
        return (2 * p - 1).Yx

    @ti.kernel
    def on_start(self):
        for I in ti.grouped(self.color):
            self.color.old[I] = ts.imageTaichi(I / self.iResolution, 0.9)

    @ti.kernel
    def on_advance(self):
        self.color.advance(self)
        self.color.update()


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()