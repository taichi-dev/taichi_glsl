from taichi_glsl import *


@ti.host_arch_only
def test_vec_fill():
    p = vec_uniform(2, int)
    q = vec_uniform(3, int)
    r = vec_uniform(4, int)

    @ti.kernel
    def func():
        p[None] = vec2(5)
        q[None] = vec3(5)
        r[None] = vec4(5)

    func()
    assert np.allclose(p.to_numpy(), np.ones(2) * 5)
    assert np.allclose(q.to_numpy(), np.ones(3) * 5)
    assert np.allclose(r.to_numpy(), np.ones(4) * 5)


@ti.host_arch_only
def test_vec_compose():
    q = vec_uniform(3, int)
    r = vec_uniform(4, int)
    s = vec_uniform(3, int)

    @ti.kernel
    def func():
        p1 = vec(2, 3)
        p2 = vec(5, 6)
        q[None] = vec(1, p1)
        r[None] = vec(p1, p2)
        s[None] = vec3(q[None])

    func()
    assert np.allclose(q.to_numpy(), np.array([1, 2, 3]))
    assert np.allclose(r.to_numpy(), np.array([2, 3, 5, 6]))
    assert np.allclose(s.to_numpy(), np.array([1, 2, 3]))


@ti.host_arch_only
def test_vec_compose_nd():
    q = vec_uniform(3, int)
    r = vec_uniform(4, int)

    @ti.kernel
    def func():
        p1 = vec2(2, 3)
        p2 = vec2(5, 6)
        q[None] = vec3(1, p1)
        r[None] = vec4(p1, p2)

    func()
    assert np.allclose(q.to_numpy(), np.array([1, 2, 3]))
    assert np.allclose(r.to_numpy(), np.array([2, 3, 5, 6]))


@ti.host_arch_only
@ti.must_throw(ValueError)
def test_vec_compose_mismatch_less():
    q = vec_uniform(3, int)

    @ti.kernel
    def func():
        p1 = vec2(2, 3)
        q[None] = vec2(1, p1)

    func()


@ti.host_arch_only
@ti.must_throw(ValueError)
def test_vec_compose_mismatch_more():
    q = vec_uniform(3, int)
    r = vec_uniform(4, int)

    @ti.kernel
    def func():
        p1 = vec2(2, 3)
        q[None] = vec4(1, p1)

    func()
