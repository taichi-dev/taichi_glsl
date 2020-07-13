**Color map**:
- blueorange (the same one used in Taichi THREE)

**SPH kernel functions**:
- spiky
- ploy6
- dspiky
- dploy6

**ODOP classes**:
- `TaichiClass` for generic base of Taichi ODOP data classes (WIP)
- `Complex` based on `TaichiClass` (use `c @ c` for multiply, WIP)

**Taichi hacks**:
- matrix.T
- vector.L, a shortcut for `vector.norm()`
- vector.L2, a shortcut for `vector.norm_sqr()`
- vector.N, a shortcut for `vector.normalized()`
- ti.pi, a shortcut for `math.pi`
- ti.tau, a shortcut for `math.tau`

**Vector math**:
- vector.Yx, a shortcut for `tl.vec(vector.y, vector.x)`, and what's more:
- If `u = tl.vec(2, 3, 4, 5)`, then `u.y_xW` is `(3, 0, 2, -5)`

**Field sampling**:
- D = tl.vec(1, 0, -1), e.g.: use `D.xyy` or `D.x__` to get `tl.vec(1, 0, 0)`
