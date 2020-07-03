import taichi as ti
import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        self.title = 'Taichi Logo'
        self.img = ti.var(ti.f32, (512, 512))

    @ti.kernel
    def on_render(self):
        for i, j in self.img:
            uv = ts.view(self.img, i, j)
            self.img[i, j] = ts.imageTaichi(uv)


MyAnimation().start()
