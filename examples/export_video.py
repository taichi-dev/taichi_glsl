import taichi as ti
import taichi_glsl as ts


class MyAnimation(ts.Animation):
    def on_init(self):
        self.img = ti.Vector(3, ti.f32, (512, 512))
        self.define_input()
        self.set_output_video('/tmp/video.gif')

    @ti.kernel
    def on_render(self):
        for I in ti.grouped(self.img):
            uv = I / self.iResolution
            self.img[I] = ti.cos(uv.xyx + self.iTime +
                                 ts.vec(0, 2, 4)) * 0.5 + 0.5


MyAnimation().start()
