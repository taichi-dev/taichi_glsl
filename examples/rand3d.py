import taichi as ti

from taichi_glsl import ts


class MyAnimation(ts.Animation):
    def on_init(self):
        self._resolution = 512
        self.img = ts.vec_array(3, float, self.iResolution, self.iResolution)

    @ti.kernel
    def on_render(self):
        for i, j in self.img:
            self.img[i, j] *= 0.94

        for i in range(200):
            p = 0.5 + 0.3 * ts.randUnit3D()
            self.img[int(ts.shuffle(p, 0, 1) * self.iResolution + 0.5)][0] = 1
            self.img[int(ts.shuffle(p, 1, 2) * self.iResolution + 0.5)][1] = 1
            self.img[int(ts.shuffle(p, 2, 0) * self.iResolution + 0.5)][2] = 1


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
