import taichi as ti
import taichi_glsl as ts

ti.init()


class MyAnimation(ts.Animation):
    def on_init(self):
        self.N = 65536
        self.dt = 0.01
        self.pos = ti.Vector(2, ti.f32, self.N)
        self.vel = ti.Vector(2, ti.f32, self.N)
        self.circles = self.pos  # alias to make ts.Animation know
        self.gravity = ti.Vector(2, ti.f32, ())
        self.attract_strength = ti.var(ti.f32, ())
        self.attract_pos = ti.Vector(2, ti.f32, ())
        self.resolution = (512, 512)
        self.title = 'Particles'
        self.define_input()

    @ti.kernel
    def on_start(self):
        self.gravity[None] = ts.vec(0.0, -1.0)
        for i in self.pos:
            self.pos[i] = ts.randND(2)
            self.vel[i] = ts.randSolid2D()

    def on_clicking(self, x, y, btn):
        self.attract_strength[None] = 2 if btn == ti.GUI.LMB else -2
        self.attract_pos[None] = [x, y]

    def on_not_clicking(self, x, y):
        self.attract_strength[None] = 0

    def on_pressing(self, key):
        if key == 'a':
            self.gravity[None] = [-1, 0]
        if key == 'd':
            self.gravity[None] = [+1, 0]
        if key == 's':
            self.gravity[None] = [0, -1]
        if key == 'w':
            self.gravity[None] = [0, +1]

    @ti.kernel
    def on_render(self):
        for i in self.pos:
            acc = self.gravity[None]
            dir = ts.normalize(self.attract_pos[None] - self.pos[i])
            acc += dir * self.attract_strength[None]
            self.vel[i] += acc * self.dt
        for i in self.pos:
            self.vel[i] = ts.boundaryReflect(self.pos[i], self.vel[i],
                    0, 1, 0.8)
        for i in self.pos:
            self.pos[i] += self.vel[i] * self.dt


MyAnimation().start()
