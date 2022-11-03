from collections.abc import MutableMapping
from operator import itemgetter

from BiTree import BiTree
from NonTree import NonTree
from QuadTree import QuadTree


class TreeMap(MutableMapping):

    def __init__(self, rect, lvl=None, bucket=20, mode=9, extend_dict=None):
        if lvl is not None and lvl < 0:
            raise ValueError(f'lvl must be >= 0 or None, not {lvl}')

        if bucket < 1:
            raise ValueError(f'bucket must be >= 1, not {bucket}')

        if mode not in (2, 4, 9):
            raise ValueError(f'mode must be in (2, 4, 9), not {mode}')

        if mode == 9:
            self.root = NonTree(rect, lvl, bucket)
        elif mode == 4:
            self.root = QuadTree(rect, lvl, bucket)
        elif mode == 2:
            self.root = BiTree(rect, lvl, bucket)

        self._d = {}

        if extend_dict:
            self.extend(extend_dict)

    def __repr__(self):
        name = type(self).__qualname__
        root = self.root
        extend = self._d.__repr__() if self._d else None
        return f"{name}({root.rect}, lvl={root.lvl}, bucket={root.bucket}, mode={root.MODE}, extend_dict={extend})"

    def __str__(self):
        return self._d.__str__()

    def __len__(self):
        return self._d.__len__()

    def __getitem__(self, point):
        return self._d.__getitem__(point)[0]  # might raise KeyError

    def __setitem__(self, point, value):
        self._d.__setitem__(point, [value])
        self.root.add(point)

    def __delitem__(self, point):
        self._d.__delitem__(point)  # might raise KeyError
        self.root.discard(point)

    def __iter__(self):
        return self._d.__iter__()

    def __reversed__(self):
        return self._d.__reversed__()

    def __contains__(self, point):
        return self._d.__contains__(point)

    def keys(self):
        return self._d.keys()

    def clear(self):
        self._d.clear()
        self.root.del_encompassed()

    def copy(self):
        tm = TreeMap(self.root.rect, lvl=self.root.lvl, bucket=self.root.bucket, mode=self.root.MODE,
                     extend_dict=self._d)
        return tm

    def get_rect(self, rect):
        ret = self.root.get_rect(rect)
        out = []
        for sublist in itemgetter(*ret)(self._d):
            out += sublist
        return out

    def get_circle(self, circ):
        ret = self.root.get_circle(circ)
        out = []
        for sublist in itemgetter(*ret)(self._d):
            out += sublist
        return out

    def get_point(self, point):
        try:
            return self._d[point].copy()
        except KeyError:
            return []

    def test_rect(self, rect):
        return self.root.test_rect(rect)

    def test_circle(self, circ):
        return self.root.test_circle(circ)

    def test_point(self, point):
        return point in self._d

    def del_rect(self, rect):
        ret = self.root.del_rect(rect)
        for point in ret:
            del self[point]
        return bool(ret)

    def del_circle(self, circ):
        ret = self.root.del_circle(circ)
        for point in ret:
            del self[point]
        return bool(ret)

    def del_point(self, point):
        try:
            del self[point]
        except KeyError:
            return False
        else:
            return True

    def pop_point(self, point, default=...):
        try:
            ret = self._d.pop(point)
            self.root.discard(point)
            return ret
        except KeyError as e:
            if default is ...:
                raise e
            return default

    def add(self, point, value):
        self._d.setdefault(point, []).append(value)
        self.root.add(point)

    def add_datapoints(self, datapoints):
        for dp in datapoints:
            self.add(dp[0], dp[1])

    def extend(self, extend_dict):
        for k, v in extend_dict:
            for val in v:
                self.add(k, val)

    def discard(self, point, value):
        try:
            self._d[point].remove(value)
        except KeyError:
            pass
        else:
            if not self._d[point]:  # empty list
                del self[point]

    def discard_datapoints(self, datapoints):
        for dp in datapoints:
            self.discard(dp[0], dp[1])

    def datapoints(self):
        for k, v in self._d.items():
            for val in v:
                yield k, val

    def data(self):
        for v in self._d.values():
            for val in v:
                yield val

    def prune(self):
        self.root.prune()
