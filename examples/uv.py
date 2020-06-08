from taichi_glsl import *

image = vec_array(3, float, 512, 512)


@ti.kernel
def paint():
    for i, j in image:
        coor = view(image, i, j)
        image[i, j] = vec(coor.x, coor.y, 0.0)


paint()
ti.imshow(image)
