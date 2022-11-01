from operator import itemgetter

from BiTree import BiTree
from NonTree import NonTree
from QuadTree import QuadTree


class TreeMap:

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

        self.d = {}

    def __repr__(self):
        name = type(self).__qualname__
        return f"{name}({self.root.rect}, lvl={self.root.lvl}, bucket={self.root.bucket}, mode={self.root.MODE})"

    def __str__(self):
        return self.d.__str__()

    def __len__(self):
        return self.d.__len__()

    def __getitem__(self, point):
        return tuple(self.d.__getitem__(point))  # might raise KeyError

    def __setitem__(self, point, value):
        self.d.setdefault(point, []).append(value)
        self.root.add(point)

    def __delitem__(self, point):
        self.d.__delitem__(point)  # might raise KeyError
        self.root.remove(point)

    def __iter__(self):
        return self.d.__iter__()

    def __reversed__(self):
        return self.d.__reversed__()

    def __contains__(self, point):
        return self.d.__contains__(point)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        return self.d.keys()

    def clear(self):
        self.d.clear()
        self.root.del_from_encompassed()

    def pop(self, point, *args):
        k = self.d.pop(point, *args)  # might raise KeyError
        self.root.remove(point)
        return k

    def popitem(self):
        k, v = self.d.popitem()  # might raise KeyError if empty
        self.root.remove(k)
        return k, tuple(v)

    def setdefault(self, point, default=None):
        try:
            return self[point]
        except KeyError:
            self[point] = default
            return default

    def values(self):
        for v in self.d.values():
            yield tuple(v)

    def items(self):
        for k, v in self.d.items():
            yield k, tuple(v)

    def copy(self):
        tm = TreeMap(self.root.rect, lvl=self.root.lvl, bucket=self.root.bucket, mode=self.root.MODE)
        for k, v in self.d.items():
            for val in v:
                tm[k] = val
        return tm

    def get_from_rect(self, rect):
        ret = self.root.get_from_rect(rect)
        return itemgetter(*ret)(self)

    def get_from_circle(self, circ):
        ret = self.root.get_from_circle(circ)
        return itemgetter(*ret)(self)

    def get_from_point(self, point):
        return self.get(point, ())

    def test_from_rect(self, rect):
        return self.root.test_from_rect(rect)

    def test_from_circle(self, circ):
        return self.root.test_from_circle(circ)

    def test_from_point(self, point):
        return point in self.keys

    def del_from_rect(self, rect):
        for point in self.root.del_from_rect(rect):
            del self.d[point]

    def del_from_circle(self, circ):
        for point in self.root.del_from_circle(circ):
            del self.d[point]

    def del_from_point(self, point):
        try:
            del self.d[point]
        except KeyError:
            pass
        else:
            self.root.remove(point)

    def test_and_del_from_point(self, point):
        try:
            del self.d[point]
        except KeyError:
            return False
        else:
            self.root.remove(point)
            return True

    def add(self, point, value):
        self[point] = value

    def add_datapoints(self, datapoints):
        for dp in datapoints:
            self.add(dp[0], dp[1])

    def remove(self, point, value):
        try:
            self.d[point].remove(value)
        except KeyError:
            pass
        else:
            if not self[point]:  # empty list
                del self[point]

    def remove_datapoints(self, datapoints):
        for dp in datapoints:
            self.remove(dp[0], dp[1])

    def get_datapoints(self):
        for k, v in self.d.items():
            for val in v:
                yield k, val

    def get_data(self):
        for v in self.d.values():
            for val in v:
                yield val

    def prune(self):
        self.root.prune()
