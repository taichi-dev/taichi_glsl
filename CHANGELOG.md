**Color map**:
- blueorange (the same one used in Taichi THREE)

**SPH kernel functions**:
- spiky
- ploy6
- dspiky
- dploy6

**ODOP classes**:
- Complex (use `c @ c` for complex multiply, experimental)

**Field sampling**:
- D = tl.vec(1, 0, -1), e.g.: `D.xyy` to get `tl.vec(1, 0, 0)`

**Taichi hacks**:
- matrix.T
- vector.L, a shortcut for `vector.norm()`
- vector.L2, a shortcut for `vector.norm_sqr()`
- vector.N, a shortcut for `vector.normalized()`
- ti.pi, a shortcut for `math.pi`
- ti.tau, a shortcut for `math.tau`
- vector.Yx, a shortcut for `tl.vec(vector.y, vector.x)`, and more :)
