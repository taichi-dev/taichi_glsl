**Field sampling**:
- sample (nearest+clamp sample)
- bilerp (bilinear+clamp sample)
- superSample2x2 (anti-aliasing)

**Particle simulation**:
- ballBoundReflect

**Painting helpers**:
- paintArrow
- sdLine

**Builtin images**:
- imageTaichi (from `taichi/examples/taichi_logo.py`)
- imageChess (NxN black-white checkers)
- imageGrid (NxN black stroke grid)

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
