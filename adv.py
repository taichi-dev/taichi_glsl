import taichi as ti
import taichi_glsl as tl
import matplotlib.cm as cm
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


dye = Pair(lambda: ti.var(ti.f32, (N, N)))
pre = Pair(lambda: ti.var(ti.f32, (N, N)))
vel = Pair(lambda: ti.Vector(2, ti.f32, (N, N)))
div = ti.var(ti.f32, (N, N))


@ti.kernel
def initdye():
    for I in ti.grouped(dye.o):
        dye.o[I] = tl.imageChess(I / N)

@ti.kernel
def initrotv():
    for I in ti.grouped(dye.o):
        vel.o[I] = (I - N / 2).yx * tl.D.zx


@ti.kernel
def advect(fn: ti.template(), f: ti.template(), v: ti.template()):
    for I in ti.grouped(f):
        btI = I - v[I] * dt
        fn[I] = tl.bilerp(f, btI)


@ti.kernel
def compute_div(v: ti.template()):
    for I in ti.grouped(v):
        l = tl.sample(v, I + tl.D.zy).x
        r = tl.sample(v, I + tl.D.xy).x
        b = tl.sample(v, I + tl.D.yz).y
        t = tl.sample(v, I + tl.D.yx).y
        d = r - l + t - b
        div[I] = d * (0.5 / dx)


@ti.kernel
def jacobi(pn: ti.template(), p: ti.template()):
    for I in ti.grouped(p):
        l = tl.sample(p, I + tl.D.zy)
        r = tl.sample(p, I + tl.D.xy)
        b = tl.sample(p, I + tl.D.yz)
        t = tl.sample(p, I + tl.D.yx)
        sa = r + l + t + b
        pn[I] = (sa - dx**2 * div[I]) * 0.25


@ti.kernel
def subgrad(v: ti.template(), p: ti.template()):
    for I in ti.grouped(v):
        l = tl.sample(p, I + tl.D.zy)
        r = tl.sample(p, I + tl.D.xy)
        b = tl.sample(p, I + tl.D.yz)
        t = tl.sample(p, I + tl.D.yx)
        g = tl.vec(r - l, t - b)
        v[I] = v[I] - g * (0.5 / dx)


@ti.kernel
def pump(v: ti.template(), d: ti.template(), a: ti.f32):
    pump_strength = ti.static(0.1)
    X, Y = ti.static(10, 15)
    for x, y in ti.ndrange((-X, X + 1), (-Y + 1, Y)):
        I = tl.vec(N // 2 + x, Y + y)
        s = ((Y - abs(y)) / Y * (X - abs(x)) / X) ** 2
        v[I] += tl.vecAngle(a + tl.pi / 2) * s * (pump_strength / dt) * 7.8
        d[I] += s * (dt / pump_strength) * 19.3


#initdye()
#initrotv()
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
    for _ in range(30):
        jacobi(pre.n, pre.o)
        pre.swap()

    subgrad(vel.o, pre.o)

    gui.set_image(cmap(dye.o.to_numpy()))
    gui.show()
