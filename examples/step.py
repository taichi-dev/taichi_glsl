from taichi_glsl import *
import time, math

image = vec_array(3, float, 512, 512)


@ti.kernel
def paint(t: ti.f32):
    for i, j in image:
        # TODO: for coor in view(image):
        coor = view(image, i, j)
        image[i, j] = smoothstep(distance(coor, vec(0.5, 0.5)), t,
                                 t - 0.06) * vec(coor.x, coor.y, 0.0)


with ti.GUI('Step UV') as gui:
    while not gui.get_event(ti.GUI.ESCAPE, ti.GUI.EXIT):
        paint(0.4 + 0.4 * math.cos(time.time() % 10000))
        gui.set_image(image)
        gui.show()
