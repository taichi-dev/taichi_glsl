import taichi as ti
import taichi_glsl as tl
import matplotlib.cm as cm

ti.init()


class MyAnimation(tl.Animation):
    def on_init(self, n=512):
        self.n = n
        self.title = 'Fractal'
        self.img = ti.var(ti.f32, (self.n * 2, self.n))
        self.colormap = cm.get_cmap('magma')
        self.define_input()

    @ti.kernel
    def on_render(self):
        for p in ti.grouped(self.img):
            c = tl.Complex(-0.8, ti.cos(self.iTime) * 0.2)
            z = tl.Complex(p / self.n - tl.vec(1, 0.5)) @ 2
            iterations = 0
            while z.mag2 < 4 and iterations < 50:
                z = z @ z + c
                iterations += 1
            self.img[p] = 1 - iterations * 0.02


MyAnimation().start()

