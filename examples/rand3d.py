from taichi_glsl import *

res = 512

img = vec_array(3, float, res, res)


@ti.kernel
def render():
    for i, j in img:
        img[i, j] *= 0.94
    for i in range(200):
        p = 0.5 + 0.3 * randUnit3D()
        img[int(shuffle(p, 0, 1) * res + 0.5)][0] = 1
        img[int(shuffle(p, 1, 2) * res + 0.5)][1] = 1
        img[int(shuffle(p, 2, 0) * res + 0.5)][2] = 1


gui = ti.GUI('Random')
while not gui.get_event(ti.GUI.ESCAPE):
    render()
    gui.set_image(img)
    gui.show()
