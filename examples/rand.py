from taichi_glsl import *

res = 512

img = array(float, res, res)


@ti.kernel
def render():
    for i, j in img:
        img[i, j] *= 0.94
    for i in range(200):
        #p = randND(2)
        #p = 0.5 + 0.3 * randUnit2D()
        p = 0.5 + 0.3 * randSolid2D()
        img[int(p * res + 0.5)] = 1


gui = ti.GUI('Random')
while not gui.get_event(ti.GUI.ESCAPE):
    render()
    gui.set_image(img)
    gui.show()
