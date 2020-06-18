'''
Some helper functions that might be useful in physics simulation.
'''

import taichi as ti


@ti.func
def momentumExchange(v1, v2, disp, m1=1, m2=1, gamma=1):
    '''
    Exchange momentum (bounce) between two objects.

    `momentumExchange` should be invocated when a bounce occurred.
    It takes the velocity of two objects before bounce, and returns the
    velocity of two objects after bounce.

    This function is most useful in rigid-body simulation with collision.
    For example::

        if distance(pos[i], pos[j]) < radius[i] + radius[j]:
            # Collision detected! Perform a momentum exchange:
            vel[i], vel[j] = momentumExchange(
                vel[i], vel[j], mass[i], mass[j], pos[i] - pos[j], 0.8)

    :parameter v1: (Vector)
        The velocity vector of the first object to bounce.
        Or, the velocity vector at the collision point in first object.

    :parameter v2: (Vector)
        The velocity vector of the second object to bounce.
        Or, the velocity vector at the collision point in second object.

    :parameter disp: (Vector)
        The displacement vector from between two object.
        Or, the normal vector of collision surface.
        Specifically, for balls or circles, `disp` is `pos1 - pos2`.

    :parameter m1: (scalar)
        The mass of the first object to bounce.

    :parameter m2: (scalar)
        The mass of the second object to bounce.

    :parameter gamma: (scalar)
        The decrease factor of bounce, in range [0, 1], determines how
        much energy is conserved after the bounce process. If 1, then
        no energy is loss; if 0, then the collided objects will stops
        immediately.

    :return: (tuple of Vector)
        The return value is a tuple of velocity of two objects after bounce.
        Specifically the first element is for the velocity of first object
        (previously to be `v1`), and same to the second element.

    :note:
        For usage example, check out this:
        https://github.com/taichi-dev/taichi_three/blob/master/examples/many_balls.py
    '''
    vel1 = v1.dot(disp)
    vel2 = v2.dot(disp)

    sm1 = ti.sqrt(m1)
    sm2 = ti.sqrt(m2)
    itsm = 1 / ti.sqrt(m1 + m2)

    kero1 = vel1 * sm1
    kero2 = vel2 * sm2

    smd1 = sm2 * itsm
    smd2 = -sm1 * itsm

    kos = 2 * (kero1 * smd1 + kero2 * smd2)
    kero1 -= kos * smd1
    kero2 -= kos * smd2

    vel1 = kero1 / sm1
    vel2 = kero2 / sm2

    disp *= gamma

    v1 -= v1.dot(disp) * disp
    v2 -= v2.dot(disp) * disp

    v1 += vel1 * disp
    v2 += vel2 * disp

    return v1, v2
