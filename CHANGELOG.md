**Field sampling**:
- sample (nearest+clamp sample)
- bilerp (bilinear+clamp sample)
- superSample2x2 (anti-aliasing)

**Vector math**:
- normalizePow (use `normalizePow(x_ij, -2)` to calcuate gravity)

**Painting helpers**:
- paintArrow (simply feed the image tensor)
- sdLine (SDF of a line segment)

**Builtin images**:
- imageTaichi (from `taichi/examples/taichi_logo.py`)
- imageChess (NxN black-white checkers)
- imageGrid (NxN black stroke grid)

**Particle simulation**:
- ballBoundReflect (often used in cloth simulation)

**Color mapping**:
- grayscale
- normalmap

**GUI base class**:
- Set `self.auto_clean = True` to clear image before `on_render`.

**Taichi hacks**:
- Turn off the annoying deprecation warning by default.
- No error on `vector = scalar`, use `vector.fill(scalar)` by default.
- `vector.product()` to get the product of all elements.
- `ti.static` now accept any argument types.
