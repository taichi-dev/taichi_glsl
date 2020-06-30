'''
Enhanced Taichi Objective Data-Oriented Programming (ODOP)
'''

import taichi as ti


@ti.data_oriented
class DataOriented:
    pass


@ti.data_oriented
class TaichiClass:
    is_taichi_class = True

    def __init__(self, *entries):
        self.entries = entries

    @classmethod
    @ti.python_scope
    def var(cls, *args, **kwargs):
        var_list = cls._var(*args, **kwargs)
        if not isinstance(var_list, (list, tuple)):
            var_list = [var_list]
        return cls(*var_list)

    @classmethod
    def _var(cls):
        raise NotImplementedError

    def _subscript(self, *indices):
        args = [ti.subscript(e, *indices) for e in self.entries]
        return self.__class__(*args)

    @ti.taichi_scope
    def subscript(self, *indices):
        return self._subscript(*indices)

    def loop_range(self):
        return self.entries[0].loop_range()

    def get_tensor_members(self):
        ret = []
        for e in self.entries:
            if hasattr(e, 'get_tensor_members'):
                e = e.get_tensor_members()
            else:
                e = [e]
            ret += e
        return ret

    @ti.taichi_scope
    def variable(self):
        return self.__class__(*(e.variable() for e in self.entries))
