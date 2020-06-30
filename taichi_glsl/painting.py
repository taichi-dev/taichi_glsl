import taichi as ti
import taichi_glsl as ts
import math


@ti.func
def sdLine(u, v, p):
    pu = p - u
    vp = v - p
    vu = v - u
    puXvu = pu.cross(vu)
    puOvu = pu.dot(vu)
    vpOvu = vp.dot(vu)
    ret = 0.0
    if puOvu < 0:
        ret = ts.length(pu)
    elif vpOvu < 0:
        ret = ts.length(vp)
    else:
        ret = puXvu * ts.invLength(vu)
    return ret

@ti.func
def paintArrow(img: ti.template(), orig, dir):
    res = ts.vec(*img.shape)
    I = orig * res
    D = dir * res
    J = I + D
    W = 3
    DL = ts.length(D)
    S = min(22, DL * 0.5)
    DS = D / (DL + 1e-4) * S
    SW = S + W
    D1 = ti.Matrix.rotation2d(+math.pi * 3 / 4) @ DS
    D2 = ti.Matrix.rotation2d(-math.pi * 3 / 4) @ DS
    bmin, bmax = ti.floor(min(I, J)), ti.ceil(max(I, J))
    for P in ti.grouped(ti.ndrange((bmin.x - SW, bmax.x + SW), (bmin.y - SW, bmax.y + SW))):
        c0 = ts.smoothstep(abs(sdLine(I, J, P)), W, W / 2)
        c1 = ts.smoothstep(abs(sdLine(J, J + D1, P)), W, W / 2)
        c2 = ts.smoothstep(abs(sdLine(J, J + D2, P)), W, W / 2)
        img[P] = max(c0, c1, c2)
