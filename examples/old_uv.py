from taichi_glsl import *

image = vec_array(3, float, 512, 512)


@ti.kernel
def paint():
    for i, j in image:
        coor = view(image, i, j)
        image[i, j] = vec(coor.xy, 0.0)


if __name__ == '__main__':
    paint()
    ti.imshow(image)
