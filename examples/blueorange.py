import taichi as ti
import taichi_glsl as tl

ti.init()


class MyAnimation(tl.Animation):
    def on_init(self, n=320):
        self.n = n
        self.title = 'Julia Set'
        self.img = ti.Vector(3, ti.f32, (self.n * 2, self.n))
        self.define_input()

    @ti.kernel
    def on_render(self):
        for p in ti.grouped(self.img):
            c = tl.Complex(self.iMouse * 2 - 1)
            z = tl.Complex(p / self.n - tl.vec(1, 0.5)) @ 2
            iterations = 0
            while z.mag2 < 4 and iterations < 50:
                z = z @ z + c
                iterations += 1
            self.img[p] = tl.blueorange(1 - iterations * 0.02)


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
