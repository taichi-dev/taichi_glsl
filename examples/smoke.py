import matplotlib.cm as cm
import taichi as ti

import taichi_glsl as ts

ti.init(arch=ti.gpu)

cmap = cm.get_cmap('magma')

N = 512
dx = 1 / N
dt = 0.001


class Pair:
    def __init__(self, f):
        self.n = f()
        self.o = f()

    def swap(self):
        self.n, self.o = self.o, self.n


dye = Pair(lambda: ts.array(float, N, N))
pre = Pair(lambda: ts.array(float, N, N))
vel = Pair(lambda: ti.Vector(2, ti.f32, (N, N)))
div = ts.array(float, N, N)


@ti.kernel
def initdye():
    for I in ti.grouped(dye.o):
        dye.o[I] = ts.imageChess(I / N)


@ti.kernel
def initrotv():
    for I in ti.grouped(dye.o):
        vel.o[I] = (I - N / 2).yx * ts.D.zx


@ti.func
def backtrace(v: ti.template(), I, dt):
    midI = I - 0.5 * ts.bilerp(v, I) * dt
    finI = I - dt * ts.bilerp(v, midI)
    return finI


@ti.kernel
def advect(fn: ti.template(), f: ti.template(), v: ti.template()):
    for I in ti.grouped(f):
        btI = backtrace(v, I, dt)
        ftI = backtrace(v, btI, -dt)
        f_btI = ts.bilerp(f, btI)
        f_ftI = ts.bilerp(f, ftI)
        fn[I] = f_btI + 0.5 * (f_ftI - f[I])


@ti.kernel
def compute_div(v: ti.template()):
    for I in ti.grouped(v):
        l = ts.sample(v, I + ts.D.zy).x
        r = ts.sample(v, I + ts.D.xy).x
        b = ts.sample(v, I + ts.D.yz).y
        t = ts.sample(v, I + ts.D.yx).y
        d = r - l + t - b
        div[I] = d * (0.5 / dx)


@ti.kernel
def jacobi(pn: ti.template(), p: ti.template()):
    for I in ti.grouped(p):
        l = ts.sample(p, I + ts.D.zy)
        r = ts.sample(p, I + ts.D.xy)
        b = ts.sample(p, I + ts.D.yz)
        t = ts.sample(p, I + ts.D.yx)
        sa = r + l + t + b
        pn[I] = (sa - dx ** 2 * div[I]) * 0.25


@ti.kernel
def gauss_seidel(pn: ti.template(), p: ti.template()):
    for I in ti.grouped(p):
        if I.sum() % 2 == 0:
            l = ts.sample(p, I + ts.D.zy)
            r = ts.sample(p, I + ts.D.xy)
            b = ts.sample(p, I + ts.D.yz)
            t = ts.sample(p, I + ts.D.yx)
            sa = r + l + t + b
            pn[I] = (sa - dx ** 2 * div[I]) * 0.25
    for I in ti.grouped(p):
        if I.sum() % 2 == 1:
            l = ts.sample(pn, I + ts.D.zy)
            r = ts.sample(pn, I + ts.D.xy)
            b = ts.sample(pn, I + ts.D.yz)
            t = ts.sample(pn, I + ts.D.yx)
            sa = r + l + t + b
            pn[I] = (sa - dx ** 2 * div[I]) * 0.25


@ti.kernel
def subgrad(v: ti.template(), p: ti.template()):
    for I in ti.grouped(v):
        l = ts.sample(p, I + ts.D.zy)
        r = ts.sample(p, I + ts.D.xy)
        b = ts.sample(p, I + ts.D.yz)
        t = ts.sample(p, I + ts.D.yx)
        g = ts.vec(r - l, t - b)
        v[I] = v[I] - g * (0.5 / dx)


@ti.kernel
def pump(v: ti.template(), d: ti.template(), a: ti.f32):
    pump_strength = ti.static(0.1)
    X, Y = ti.static(15, 15)
    for x, y in ti.ndrange((-X, X + 1), (-Y + 1, Y)):
        I = ts.vec(N // 2 + x, Y + y)
        s = ((Y - abs(y)) / Y * (X - abs(x)) / X) ** 2
        v[I] += ts.vecAngle(a + ts.pi / 2) * s * (pump_strength / dt) * 7.8
        d[I] += s * (dt / pump_strength) * 21.3


if __name__ == '__main__':
    gui = ti.GUI('advect', N)
    while gui.running:
        for e in gui.get_events(gui.PRESS):
            if e.key == gui.ESCAPE:
                gui.running = False

        if not gui.is_pressed(gui.SPACE):
            a = 0
            if gui.is_pressed('a', gui.LEFT):
                a += 0.7
            if gui.is_pressed('d', gui.RIGHT):
                a -= 0.7
            pump(vel.o, dye.o, a)

        advect(dye.n, dye.o, vel.o)
        advect(vel.n, vel.o, vel.o)
        dye.swap()
        vel.swap()

        compute_div(vel.o)
        for _ in range(5):
            jacobi(pre.n, pre.o)
            pre.swap()

        for _ in range(20):
            gauss_seidel(pre.n, pre.o)
            pre.swap()

        subgrad(vel.o, pre.o)

        gui.set_image(cmap(dye.o.to_numpy()))
        gui.show()
