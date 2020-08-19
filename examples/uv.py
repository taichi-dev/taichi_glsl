from taichi_glsl import *

ti.init()


class MyAnimation(Animation):
    def on_init(self):
        self.title = 'UV'
        self.img = vec_array(3, float, 512, 512)

    @ti.kernel
    def on_render(self):
        for i, j in self.img:
            uv = view(self.img, i, j)
            self.img[i, j] = vec(uv.xy, 0.0)


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
