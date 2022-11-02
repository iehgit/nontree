from collections.abc import MutableMapping
from operator import itemgetter
from itertools import chain

from BiTree import BiTree
from NonTree import NonTree
from QuadTree import QuadTree


class TreeMap(MutableMapping):

    def __init__(self, rect, lvl=None, bucket=20, mode=9):
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

    def __repr__(self):
        name = type(self).__qualname__
        root = self.root
        return f"{name}({root.rect}, lvl={root.lvl}, bucket={root.bucket}, mode={root.MODE})"

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
        self.root.remove(point)

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
        self.root.del_from_encompassed()

    def copy(self):
        tm = TreeMap(self.root.rect, lvl=self.root.lvl, bucket=self.root.bucket, mode=self.root.MODE)
        tm.add_datapoints(self.get_datapoints())
        return tm

    def get_from_rect(self, rect):
        ret = self.root.get_from_rect(rect)  # TODO return List, perf list(chain(itemgetter))) vs comprehension,
        return chain(itemgetter(*ret)(self._d))  # TODO itertools.chain.from_iterable

    def get_from_circle(self, circ):
        ret = self.root.get_from_circle(circ)
        return chain(itemgetter(*ret)(self._d))

    def get_from_point(self, point):
        try:
            return tuple(self._d[point])
        except KeyError:
            return ()

    def test_from_rect(self, rect):
        return self.root.test_from_rect(rect)

    def test_from_circle(self, circ):
        return self.root.test_from_circle(circ)

    def test_from_point(self, point):
        return point in self._d.keys

    def del_from_rect(self, rect):
        for point in self.root.del_from_rect(rect):
            del self[point]

    def del_from_circle(self, circ):
        for point in self.root.del_from_circle(circ):
            del self[point]

    def del_from_point(self, point):
        try:
            del self[point]
        except KeyError:
            pass

    def test_and_del_from_point(self, point):
        try:
            del self[point]
        except KeyError:
            return False
        else:
            return True

    def add(self, point, value):
        self._d.setdefault(point, []).append(value)
        self.root.add(point)

    def add_datapoints(self, datapoints):
        for dp in datapoints:
            self.add(dp[0], dp[1])

    def remove(self, point, value):
        try:
            self._d[point].remove(value)
        except KeyError:
            pass
        else:
            if not self._d[point]:  # empty list
                del self[point]

    def remove_datapoints(self, datapoints):
        for dp in datapoints:
            self.remove(dp[0], dp[1])

    def get_datapoints(self):
        for k, v in self._d.items():
            for val in v:
                yield k, val

    def get_data(self):
        for v in self._d.values():
            for val in v:
                yield val

    def prune(self):
        self.root.prune()
