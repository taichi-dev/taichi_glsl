from taichi_glsl import *

ti.init(ti.gpu)
ti.core.toggle_advanced_optimization(False)

dt = 0.01
N = 100
W0 = 0.6
L0 = W0 / N
K0 = 100
D0 = 0.01
G0 = 0.00005
A0 = 0.0001
B0 = 0.2

pos = vec_tensor(2, float)
vel = vec_tensor(2, float)
cir_pos = vec_tensor(2, float)
attr_pos = vec_tensor(2, float)
attr_stren = tensor(float)
cir_radius = tensor(float)
ti.root.dense(ti.ij, (N, N)).place(pos, vel)
ti.root.place(cir_pos, cir_radius, attr_pos, attr_stren)


@ti.func
def reaction(I, J, k):
    ret = pos[I] * 0
    if all(J < N) and all(J >= 0):
        dis = pos[I] - pos[J]
        ret = K0 * normalize(dis) * (k * L0 - length(dis))
    return ret


@ti.kernel
def substep():
    for I in ti.grouped(pos):
        acc = reaction(I, I + vec(0, 1), 1)
        acc += reaction(I, I - vec(0, 1), 1)
        acc += reaction(I, I + vec(1, 0), 1)
        acc += reaction(I, I - vec(1, 0), 1)
        acc += reaction(I, I + vec(1, 1), math.sqrt(2))
        acc += reaction(I, I - vec(1, 1), math.sqrt(2))
        acc += reaction(I, I + vec(1, -1), math.sqrt(2))
        acc += reaction(I, I - vec(1, -1), math.sqrt(2))
        acc[1] -= G0
        acc += attr_stren[None] * normalize(attr_pos[None] - pos[I])
        vel[I] *= exp(-dt * D0)
        vel[I] += acc * dt

    for I in ti.grouped(pos):
        d = pos[I] - cir_pos[None]
        d1 = length(d)
        if d1 <= cir_radius[None]:
            d /= d1
            vod = dot(vel[I], d)
            if vod < 0:
                vel[I] -= 2 * d * vod

    for I in ti.grouped(pos):
        if vel[I][0] < 0 and pos[I][0] < 0:
            vel[I][0] *= -B0
        if vel[I][0] > 0 and pos[I][0] > 1:
            vel[I][0] *= -B0
        if vel[I][1] < 0 and pos[I][1] < 0:
            vel[I][1] *= -B0
        if vel[I][1] > 0 and pos[I][1] > 1:
            vel[I][1] *= -B0

    for I in ti.grouped(pos):
        pos[I] += vel[I] * dt


@ti.kernel
def init():
    cir_pos[None] = vec(0.5, 0.0)
    cir_radius[None] = 0.1
    for I in ti.grouped(pos):
        pos[I] = I / N * W0 + (1 - W0) / 2


init()

print('[Hint] LMB/RMB to attract/repel, MMB to set circle position')
gui = ti.GUI('Mass-spring block')
while True:
    if gui.get_event(ti.GUI.PRESS, 'WMClose'):
        if gui.event.key == ti.GUI.ESCAPE:
            exit()
        elif gui.event.key == ti.GUI.MMB:
            cir_pos[None] = gui.event.pos
    if gui.is_pressed(ti.GUI.LMB):
        attr_pos[None] = gui.get_cursor_pos()
        attr_stren[None] = A0
    elif gui.is_pressed(ti.GUI.RMB):
        attr_pos[None] = gui.get_cursor_pos()
        attr_stren[None] = -A0
    else:
        attr_stren[None] = 0
    for i in range(120):
        substep()
    gui.circles(pos.to_numpy().reshape(N**2, 2), radius=1.8)
    gui.circle(cir_pos[None], radius=cir_radius[None] * 512)
    gui.show()
