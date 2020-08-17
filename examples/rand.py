import taichi as ti

import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        self._resolution = 512
        self.img = ts.array(float, self.iResolution, self.iResolution)
    @ti.kernel
    def on_render(self):
        for i, j in self.img:
            self.img[i, j] *= 0.94

        for i in range(200):
            # Try comment and uncomment these:
            # p = randND(2)
            # p = 0.5 + 0.3 * randUnit2D()
            p = 0.5 + 0.3 * ts.randSolid2D()
            self.img[int(p * self.iResolution + 0.5)] = 1


if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
