import taichi as ti

import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        self.N = 8192
        self.dt = 0.01
        self.pos = ti.Vector(2, ti.f32, self.N)
        self.vel = ti.Vector(2, ti.f32, self.N)
        self.circles = self.pos  # alias to make ts.Animation know
        self.attract_strength = ti.var(ti.f32, ())
        self.attract_pos = ti.Vector(2, ti.f32, ())
        self.resolution = (512, 512)
        self.title = 'Particles'
        self.define_input()

    @ti.kernel
    def on_start(self):
        for i in self.pos:
            self.pos[i] = ts.randND(2)
            self.vel[i] = ts.randSolid2D()

    @ti.kernel
    def on_advance(self):
        for i in self.pos:
            acc = ts.vec(0.0, -1.0)
            if any(self.iKeyDirection):  # ASWD?
                acc = self.iKeyDirection
            if any(self.iMouseButton):
                dir = ts.normalize(self.iMouse - self.pos[i]) * 2
                if self.iMouseButton[0]:  # LMB pressed?
                    acc += dir
                if self.iMouseButton[1]:  # RMB pressed?
                    acc -= dir
            self.vel[i] += acc * self.dt
        for i in self.pos:
            self.vel[i] = ts.boundReflect(self.pos[i], self.vel[i], 0, 1, 0.8)
        for i in self.pos:
            self.pos[i] += self.vel[i] * self.dt

if __name__ == '__main__':
    animation = MyAnimation()
    animation.start()
