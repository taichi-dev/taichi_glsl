from taichi_glsl import *

ti.init(ti.opengl)

fov = math.tan(math.radians(26))
img = vec_array(3, float, 512, 512)
mouse = vec_uniform(2, float)
eps = 1e-5


@ti.func
def sdfSphere(p, c, r):
    return distance(p, c) - r


@ti.func
def mUnion(a, b):
    if a[0] > b[0]:
        a = b
    return a


@ti.func
def mIntersect(a, b):
    if a[0] < b[0]:
        a = b
    return a


@ti.func
def mScene(p):
    m = mouse[None]
    return mUnion(  #         center         rad   emi  spec diff
        vec(sdfSphere(p, vec(m.x, m.y, 0.0), 0.2), 1.0, 0.0, 0.0),
        vec(sdfSphere(p, vec(0.0, 0.0, 0.4), 0.5), 0.0, 0.0, 1.0))


@ti.func
def gradScene(p, sdf):
    return normalize(
        vec(
            mScene(p + vec(eps, 0, 0))[0],
            mScene(p + vec(0, eps, 0))[0],
            mScene(p + vec(0, 0, eps))[0]) - sdf)


@ti.func
def radiance(eye, dir):
    p = eye
    clr = vec3(0.0)
    depth = 0.0
    for i in range(60):
        res = mScene(p)
        sdf, emi, spec, diff = res
        if sdf < eps:
            clr += vec3(emi)
            if spec != 0:
                if rand() < spec:
                    norm = gradScene(p, sdf)
                    dir = reflect(dir, norm)
                    p += 2 * eps * dir
                    continue
            if diff != 0:
                if rand() < diff:
                    norm = gradScene(p, sdf)
                    dir = randUnit3D()
                    NoD = dot(dir, norm)
                    if NoD < 0:
                        dir -= 2 * NoD * norm
                    p += 2 * eps * dir
                    continue
            break
        depth += sdf
        p += sdf * dir
    return clr


@ti.kernel
def render():
    eye = vec(0.0, 0.0, -1.8)
    for i, j in img:
        coor = fov * (view(img, i, j) * 2.0 - 1.0)
        dir = normalize(vec(coor, 1.0))
        for t in range(16):
            img[i, j] += radiance(eye, dir)


mouse[None] = [-0.5, 0.5]
gui = ti.GUI('SDF-RT2')
count = 0
while gui.running:
    gui.running = not gui.get_event(gui.ESCAPE)
    if gui.is_pressed(gui.LMB):
        x, y = gui.get_cursor_pos()
        mouse[None] = [x * 2 - 1, y * 2 - 1]
        img.fill(0)
        count = 0
    render()
    gui.set_image(np.sqrt(img.to_numpy() * (1 / 16 / (count + 1))))
    gui.show()
    count += 1
