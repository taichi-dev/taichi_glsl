import taichi as ti
import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        self.title = 'Test Arrow'
        self.img = ti.var(ti.f32, (512, 512))
        self.auto_clean = True
        self.define_input()

    @ti.kernel
    def on_render(self):
        ts.paintArrow(self.img, ts.vec2(0.0), self.iMouse)


MyAnimation().start()
