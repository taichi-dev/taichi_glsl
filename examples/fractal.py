import matplotlib.cm as cm
import taichi as ti

import taichi_glsl as tl

ti.init()


class MyAnimation(tl.Animation):
    def on_init(self, n=512):
        self.n = n
        self.title = 'Julia Set'
        self.img = ti.var(ti.f32, (self.n * 2, self.n))
        self.colormap = cm.get_cmap('magma')
        self.define_input()

    @ti.kernel
    def on_render(self):
        for p in ti.grouped(self.img):
            c = tl.Complex(self.iMouse * 2 - 1)
            z = tl.Complex(p / self.n - tl.vec(1, 0.5)) @ 2
            iterations = 0
            while z.mag2 < 4 and iterations < 100:
                z = z @ z + c
                iterations += 1
            self.img[p] = 1 - iterations * 0.01


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
