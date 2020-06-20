import taichi as ti
import taichi_glsl as ts
ti.init(ti.cpu)


class singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

    def clear(self):
        self._instance = {}


@singleton
@ti.data_oriented
class Scene:
    def __init__(self, res=(512, 512),
            max_vertices=128,
            max_lines=128,
            max_triangles=128,
            ):
        self.img = ti.Vector(3, ti.f32)
        self.vertices = Vertex.var()
        self.lines = Line.var()
        self.triangles = Triangle.var()

        ti.root.dense(ti.ij, res).place(self.img)
        self.vertices_snode = ti.root.dynamic(ti.i, max_vertices)
        self.vertices_snode.place(self.vertices)
        self.lines_snode = ti.root.dynamic(ti.i, max_lines)
        self.lines_snode.place(self.lines)
        self.triangles_snode = ti.root.dynamic(ti.i, max_triangles)
        self.triangles_snode.place(self.triangles)

    @ti.func
    def add_vertex(self, pos, clr):
        i = ti.length(self.vertices_snode, [])
        self.vertices[i].pos = pos
        self.vertices[i].clr = clr
        return i

    @ti.func
    def add_line(self, idx):
        i = ti.length(self.lines_snode, [])
        self.lines[i].idx = idx
        return i

    @ti.func
    def add_triangle(self, idx):
        i = ti.length(self.lines_snode, [])
        self.triangles[i].idx = idx
        return i

    @ti.kernel
    def render(self):
        for i in self.vertices.loop_range():
            self.vertices[i].render()
        for i in self.lines.loop_range():
            self.lines[i].render()
        for i in self.triangles.loop_range():
            self.triangles[i].render()


@ti.data_oriented
class TaichiClass:
    is_taichi_class = True

    @classmethod
    def var(cls):
        raise NotImplementedError

    def get_members(self):
        raise NotImplementedError

    # multiple
    def get_tensor_members(self):
        return [x.get_tensor_members() for x in self.tensor_members()]

    # multiple
    def loop_range(self):
        return self.tensor_members()[0].loop_range()

    @classmethod
    def _make_subscript(cls, self, I):
        return cls(*(x.subscript(I) for x in self.tensor_members()))

    # multiple
    def subscript(self, I):
        return self._make_subscript(self, I)


@ti.data_oriented
class Vertex(TaichiClass):
    def __init__(self, pos, clr):
        self.pos = pos
        self.clr = clr

    @classmethod
    def var(cls):
        return cls(ti.Vector(3, ti.f32), ti.Vector(3, ti.f32))

    def tensor_members(self):
        return [self.pos, self.clr]

    @ti.func
    def render(self):
        p = self.pos.xy
        Scene().img[int(p)] = self.clr


@ti.data_oriented
class Geometry(TaichiClass):
    n_vertices = None

    def __init__(self, idx):
        self.idx = idx

    @classmethod
    def var(cls):
        return cls(ti.Vector(cls.n_vertices, ti.i32))

    def tensor_members(self):
        return [self.idx]

    @ti.func
    def get_vertex(self, i: ti.template()):
        return Scene().vertices[self.idx[i]]


@ti.data_oriented
class Line(Geometry):
    n_vertices = 2

    @ti.func
    def render_poor(self):
        # https://blog.csdn.net/qq_41883085/article/details/102730878
        scene = Scene()
        A, B = self.Axy, self.Bxy
        if abs(B.x - A.x) >= abs(B.y - A.y):
            if A.x > B.x:
                A, B = B, A
            AB = A - B
            AxB = A.cross(B)
            p = A
            sgn = ts.sign(B.y - A.y)
            for i in range(ti.floor(A.x), ti.ceil(B.x)):
                p.x += 1.0
                sdf = p.cross(AB) + AxB
                p.y += ts.step(sgn * sdf, 0.0) * sgn
                scene.img[int(p)] = ts.vec3(1.0)
        else:
            if A.y > B.y:
                A, B = B, A
            AB = A - B
            AxB = A.cross(B)
            p = A
            sgn = ts.sign(B.x - A.x)
            for i in range(ti.floor(A.y), ti.ceil(B.y)):
                p.y += 1.0
                sdf = p.cross(AB) + AxB
                p.x += ts.step(0.0, sgn * sdf) * sgn
                scene.img[int(p)] = ts.vec3(1.0)

    @ti.func
    def render(self):
        scene = Scene()
        A, B = self.get_vertex(0).pos.xy, self.get_vertex(1).pos.xy
        U, V = self.get_vertex(0).clr, self.get_vertex(1).clr
        if A.x > B.x:
            A, B = B, A
            U, V = V, U

        pos = A
        AB = B - A
        len = ts.length(AB)

        ik = min(1, len * 0.2)
        clr = U * ik
        clr_dir = (V - U) * (ik ** 2 / len)
        rlik = ts.round(len / ik)
        dir = AB / rlik
        for i in range(rlik):
            p, q = int(pos)
            u, v = ts.fract(pos)
            scene.img[p + 0, q + 0] += (1 - u) * (1 - v) * clr
            scene.img[p + 1, q + 0] += u * (1 - v) * clr
            scene.img[p + 1, q + 1] += u * v * clr
            scene.img[p + 0, q + 1] += (1 - u) * v * clr
            pos += dir
            clr += clr_dir


@ti.func
def sort3(A, B, C, key: ti.template()):
    if   key(A) <= key(B) <= key(C): pass
    elif key(A) <= key(C) <= key(B):    B, C =    C, B
    elif key(B) <= key(A) <= key(C): A, B    = B, A
    elif key(B) <= key(C) <= key(A): A, B, C = B, C, A
    elif key(C) <= key(A) <= key(B): A, B, C = C, A, B
    elif key(C) <= key(B) <= key(A): A, B, C = C, B, A
    return A, B, C


@ti.func
def sort2(A, B, key: ti.template()):
    if key(A) > key(B): A, B = B, A
    return A, B


@ti.data_oriented
class Triangle(Geometry):
    n_vertices = 3

    @staticmethod
    @ti.func
    def paint_tri(btmy, topy, topx, topu, x0, x1, u0, u1):
        scene = Scene()

        xmin, xmax = min(x0, topx), max(x1, topx)
        rbtmy, rtopy = sort2(btmy, topy, lambda x: x)
        for y in range(rbtmy, rtopy):
            yt = (y - btmy) / (topy - btmy)
            t0 = yt * (topx - x0)
            t1 = yt * (topx - x1)
            xb, xe = x0 + t0, x1 + t1
            cb, ce = ts.mix(u0, topu, yt), ts.mix(u1, topu, yt)
            for x in range(ts.floor(xb), ts.ceil(xe)):
                xt = (x - xb) / (xe - xb)
                scene.img[x, y] = ts.mix(cb, ce, xt)

    @ti.func
    def render(self):
        A, B, C = (
                self.get_vertex(0).pos.xy,
                self.get_vertex(1).pos.xy,
                self.get_vertex(2).pos.xy,
                )
        U, V, W = (
                self.get_vertex(0).clr,
                self.get_vertex(1).clr,
                self.get_vertex(2).clr,
                )

        if any(A != B) and any(B != C):
            A_, B_, C_ = sort3(
                    ts.vecND(5, A, U),
                    ts.vecND(5, B, V),
                    ts.vecND(5, C, W),
                    lambda p: p.y)
            A, U = ts.shuffle(A_, 0, 1), ts.shuffle(A_, 2, 3, 4)
            B, V = ts.shuffle(B_, 0, 1), ts.shuffle(B_, 2, 3, 4)
            C, W = ts.shuffle(C_, 0, 1), ts.shuffle(C_, 2, 3, 4)

            #print(A.y, B.y, C.y)

            xmin, xmid, xmax = sort3(A.x, B.x, C.x, lambda x: x)

            xpoint = A.x + (C.x - A.x) * (B.y - A.y) / (C.y - A.y)
            xcolor = U + (W - U) * (B.y - A.y) / (C.y - A.y)

            x0, x1 = B.x, xpoint
            u0, u1 = V,   xcolor

            if x0 > x1:
                x1, x0 = x0, x1
                u1, u0 = u0, u1

            self.paint_tri(B.y, C.y, C.x, W, x0, x1, u0, u1)
            self.paint_tri(B.y, A.y, A.x, U, x0, x1, u0, u1)



scene = Scene()

N = 3
pos = scene.vertices.pos
vel = ti.Vector(3, ti.f32, 3 * N)

@ti.kernel
def init():
    if 1:
        for t in range(N):
            i = scene.add_vertex(ts.randND(3) * 512.0, ts.vec3(1.0, 0.0, 0.0))
            j = scene.add_vertex(ts.randND(3) * 512.0, ts.vec3(0.0, 1.0, 0.0))
            k = scene.add_vertex(ts.randND(3) * 512.0, ts.vec3(0.0, 0.0, 1.0))
            vel[t * 3 + 0] = ts.vec3(ts.randUnit2D(), 0.0)
            vel[t * 3 + 1] = ts.vec3(ts.randUnit2D(), 0.0)
            vel[t * 3 + 2] = ts.vec3(ts.randUnit2D(), 0.0)
            scene.add_line(ts.vec(i, j))
            scene.add_line(ts.vec(j, k))
            scene.add_line(ts.vec(k, i))
            scene.add_triangle(ts.vec(i, j, k))

dt = 0.1
@ti.kernel
def substep():
    for i in range(3 * N):
        for j in ti.static(range(vel.n)):
            if pos[i][j] < 0 and vel[i][j] < 0:
                vel[i][j] = -vel[i][j]
            if pos[i][j] > 512 and vel[i][j] > 0:
                vel[i][j] = -vel[i][j]

        pos[i] += vel[i] * dt

init()

gui = ti.GUI('Hello')
while gui.running:
    gui.running = not gui.get_event(ti.GUI.ESCAPE)

    for i in range(20):
        substep()
    scene.img.fill(0)
    scene.render()
    gui.set_image(scene.img)
    gui.show()
