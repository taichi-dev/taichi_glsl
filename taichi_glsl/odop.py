'''
Enhanced Taichi Objective Data-Oriented Programming (ODOP)
'''

import taichi as ti


@ti.data_oriented
class DataOriented:
    pass


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
        if hasattr(e, 'get_tensor_members'):
            e = e.get_tensor_members()
        else:
            e = [e]
        ret += e

    @ti.taichi_scope
    def variable(self):
        return self.__class__(*(ti.expr_init(e) for e in self.entries))

    def snode(self):
        return self.loop_range().snode()

    @property
    def shape(self):
        return self.snode().shape

    @ti.taichi_scope
    def __ti_repr__(self):
        raise NotImplementedError

    def __repr__(self):
        ret = []
        for e in self.__ti_repr__():
            ret.append(e)
        return ''.join(map(str, ret))
