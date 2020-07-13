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
def paintArrow(img: ti.template(),
               orig,
               dir,
               color=1,
               width=3,
               max_size=12,
               min_scale=0.4):
    res = ts.vec(*img.shape)
    I = orig * res
    D = dir * res
    J = I + D
    DL = ts.length(D)
    S = min(max_size, DL * min_scale)
    DS = D / (DL + 1e-4) * S
    SW = S + width
    D1 = ti.Matrix.rotation2d(+math.pi * 3 / 4) @ DS
    D2 = ti.Matrix.rotation2d(-math.pi * 3 / 4) @ DS
    bmin, bmax = ti.floor(max(0,
                              min(I, J) - SW)), ti.ceil(
                                  min(res - 1,
                                      max(I, J) + SW))
    for P in ti.grouped(ti.ndrange((bmin.x, bmax.x), (bmin.y, bmax.y))):
        c0 = ts.smoothstep(abs(sdLine(I, J, P)), width, width / 2)
        c1 = ts.smoothstep(abs(sdLine(J, J + D1, P)), width, width / 2)
        c2 = ts.smoothstep(abs(sdLine(J, J + D2, P)), width, width / 2)
        ti.atomic_max(img[P], max(c0, c1, c2) * color)
