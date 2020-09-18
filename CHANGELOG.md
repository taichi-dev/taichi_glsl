**Hot Fixes**:

- Remove unexpected `p` and `s` directory in wheel file.

**GUI**:

- Support choosing `ipython` or `matplotlib` as backend in `ts.Animation`, e.g.:
```py
self.gui_backend = 'ipython'
```

This would allows you to display GUI result in Jupyter notebook, checkout the [config file](https://github.com/taichi-dev/taichi_glsl/blob/master/jupyter_notebook_config.py).

**Field sampling**:

- `dflSample(field, P, dfl)`: return a default value `dfl` when `P` out of range.