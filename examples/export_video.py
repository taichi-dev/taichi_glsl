import taichi as ti
import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        self.img = ti.Vector(3, ti.f32, (512, 512))
        self.set_output_video('/tmp/video.gif')
        self.define_input()

    @ti.kernel
    def on_render(self):
        for I in ti.grouped(self.img):
            uv = I / self.iResolution
            self.img[I] = ti.cos(uv.xyx + self.iTime +
                                 ts.vec(0, 2, 4)) * 0.5 + 0.5


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
