from taichi_glsl import *

ti.init()


class MyAnimation(Animation):
    def on_init(self):
        self.title = 'Step + UV'
        self.img = vec_array(3, float, 512, 512)
        self.define_input()

    @ti.kernel
    def on_render(self):
        t = 0.4 + 0.4 * cos(self.iTime)
        for i, j in self.img:
            # TODO(archibate): for coor in view(self.img):
            uv = view(self.img, i, j)
            self.img[i, j] = smoothstep(distance(uv, vec(0.5, 0.5)), t,
                                        t - 0.06) * vec(uv.x, uv.y, 0.0)


MyAnimation().start()
