from collections.abc import MutableMapping
from operator import itemgetter

from nontree.BiTree import BiTree
from nontree.NonTree import NonTree
from nontree.QuadTree import QuadTree


class TreeMap(MutableMapping):
    """The TreeMap contains a NonTree (or QuadTree, BiTree) and maps its points to payload data.\x20\x20
    A single point can map to multiple data objects.\x20\x20
    The TreeMap provides methods to make use of the underlying NonTree (or QuadTree, BiTree).\x20\x20
    It also provides a dict-ish interface.
    """

    def __init__(self, rect, lvl=None, bucket=20, mode=9, initial_dict=None):
        """
        :param rect: A rectangle in the shape of (x, y, width, height).
        :param lvl: Maximum nesting depth. None for automatic heuristic value. >= 0
        :param bucket: Maximum number of points in a tree, before it is split into subtrees. >= 1
        :param mode: Number of subtrees a tree is split into. 9: NonTree, 4: QuadTree, 2: BiTree
        :param initial_dict: A dict with points (x, y) as keys and lists of objects as values for initial filling.
        :raises ValueError: If lvl, bucket, mode is out of bounds.
        """
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

        if initial_dict:
            self.extend(initial_dict)

    def __repr__(self):
        name = type(self).__qualname__
        root = self.root
        extend = self._d.__repr__() if self._d else None
        return f"{name}({root.rect}, lvl={root.lvl}, bucket={root.bucket}, mode={root.MODE}, initial_dict={extend})"

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
        """Copies this TreeMap.

        :return: A shallow copy of this TreeMap.
        """
        tm = TreeMap(self.root.rect, lvl=self.root.lvl, bucket=self.root.bucket, mode=self.root.MODE,
                     initial_dict=self._d)
        return tm

    def get_rect(self, rect):
        """Gets payload data of all points that are within a rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :return: A list of objects.
        """
        ret = self.root.get_rect(rect)
        if not ret:
            return []

        out = []
        for sublist in itemgetter(*ret)(self._d):
            out += sublist
        return out

    def get_circle(self, circ):
        """Gets payload data of all points that are within a circle.

        :param circ: A circle in the shape of (x, y, radius).
        :return: A list of objects.
        """
        ret = self.root.get_circle(circ)
        if not ret:
            return []

        out = []
        for sublist in itemgetter(*ret)(self._d):
            out += sublist
        return out

    def get_point(self, point):
        """Gets payload data of point if it is in the tree.

        :param point: A point in the shape of (x, y).
        :return: A list of objects.
        """
        try:
            return self._d[point].copy()
        except KeyError:
            return []

    def test_rect(self, rect):
        """Tests if there are points within a rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :return: True if there are points within the rectangle, False if not.
        """
        return self.root.test_rect(rect)

    def test_circle(self, circ):
        """Tests if there are points within a circle.

        :param circ: A circle in the shape of (x, y, radius).
        :return: True if there are points within the circle, False if not.
        """
        return self.root.test_circle(circ)

    def test_point(self, point):
        """Tests if point is in the tree.

        :param point: A point in the shape of (x, y).
        :return: True if point is in the tree, False if not.
        """
        return point in self._d

    def del_rect(self, rect):
        """Deletes points within a rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :return: True if there have been points to delete, False if not.
        """
        ret = self.root.del_rect(rect)
        for point in ret:
            del self[point]
        return bool(ret)

    def del_circle(self, circ):
        """Deletes points within a circle.

        :param circ: A circle in the shape of (x, y, radius).
        :return: True if there have been points to delete, False if not.
        """
        ret = self.root.del_circle(circ)
        for point in ret:
            del self[point]
        return bool(ret)

    def del_point(self, point):
        """Deletes a point from the tree.

        :param point: A point in the shape of (x, y).
        :return: True if there has been a point to delete, False if not.
        """
        try:
            del self[point]
        except KeyError:
            return False
        else:
            return True

    def pop_point(self, point, default=...):
        """Pops a point from the tree and returns its payload data.

        :param point: A point in the shape of (x, y).
        :param default: Optional default value if point is not in tree.
        :return: A list of objects.
        :raises KeyError: If point is not in the tree, and no default is given.
        """
        try:
            ret = self._d.pop(point)
            self.root.discard(point)
            return ret
        except KeyError as e:
            if default is ...:
                raise e
            return default

    def add(self, point, value):
        """Adds payload data to a point in the tree.
        Also adds the point itself to the tree, if not yet existing.

        :param point: A point in the shape of (x, y).
        :param value: An object.
        """
        self._d.setdefault(point, []).append(value)
        self.root.add(point)

    def add_datapoints(self, datapoints):
        """Adds points with payload data to the tree.

        :param datapoints: An iterable of datapoints in the shape of ((x, y), value).
        """
        for dp in datapoints:
            self.add(dp[0], dp[1])

    def extend(self, extend_dict):
        """Extends this tree with points and payload data from a dictionary.

        :param extend_dict: A dict with points (x, y) as keys and lists of objects as values.
        """
        for k, v in extend_dict.items():
            for val in v:
                self.add(k, val)

    def discard(self, point, value):
        """Discards a payload value from a point in the tree.
        Also deletes the point if it has no payload values left.

        :param point: A point in the shape of (x, y).
        :param value: An object.
        """
        try:
            self._d[point].remove(value)
        except KeyError:
            pass
        else:
            if not self._d[point]:  # empty list
                del self[point]

    def discard_datapoints(self, datapoints):
        """Discards datapoints from the tree.

        :param datapoints:  An iterable of datapoints in the shape of ((x, y), value).
        """
        for dp in datapoints:
            self.discard(dp[0], dp[1])

    def datapoints(self):
        """An iterator over all datapoints in the tree.
        Datapoint shape: ((x, y), value)
        """
        for k, v in self._d.items():
            for val in v:
                yield k, val

    def data(self):
        """An iterator over all payload data in the tree."""
        for v in self._d.values():
            for val in v:
                yield val

    def prune(self):
        """Prunes empty sub-trees."""
        self.root.prune()
