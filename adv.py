import taichi as ti
import taichi_glsl as tl


N = 512
dt = 0.01


class Pair:
    def __init__(self, f):
        self.n = f()
        self.o = f()

    def swap(self):
        self.n, self.o = self.o, self.n


dye = Pair(lambda: ti.var(ti.f32, (N, N)))


@ti.kernel
def init():
    for I in ti.grouped(dye.o):
        dye.o[I] = tl.imageChess(I / N)


@ti.func
def velocity(P):
    return (P - N / 2).yx * tl.D.zx


@ti.kernel
def advect(fn: ti.template(), fo: ti.template()):
    for I in ti.grouped(fo):
        btI = I - velocity(I) * dt
        fn[I] = tl.bilerp(fo, btI)


init()
gui = ti.GUI('advect', N)
while gui.running:
    for e in gui.get_events(gui.PRESS):
        if e.key == gui.ESCAPE:
            gui.running = False

    advect(dye.n, dye.o)
    dye.swap()

    gui.set_image(dye.o)
    gui.show()
