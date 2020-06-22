'''
Enhanced Taichi Objective Data-Oriented Programming (ODOP)
'''

import taichi as ti


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

    @ti.func
    def _subscript(self, I):
        return self.__class__(*(e[I] for e in self.entries))

    @ti.taichi_scope
    def subscript(self, I):
        return self._subscript(I)

    @ti.func
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
