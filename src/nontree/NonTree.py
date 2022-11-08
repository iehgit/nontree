import math

try:
    import numba
except (ModuleNotFoundError, ImportError):
    def _conditional_njit(function):
        return function
else:
    def _conditional_njit(function):
        return numba.njit(cache=True)(function)


class NonTree:
    """A class for efficient collision detection of points in a sparse 2D plane.\x20\x20
    Based on the well known Quadtree data structure.\x20\x20
    This is a variant that splits each plane into 9 sub-trees in a 3 by 3 grid.
    """

    __slots__ = 'rect', 'lvl', 'bucket', 'points', 'subtrees'

    MODE = 9  # Number of subtrees a tree is split into

    def __init__(self, rect, lvl=None, bucket=20):
        """
        :param rect: A rectangle in the shape of (x, y, width, height).
        :param lvl: Maximum nesting depth. None for automatic heuristic value. >= 0
        :param bucket: Maximum number of points in a tree, before it is split into subtrees.  >= 1
        :raises ValueError: If lvl, bucket is out of bounds.
        """
        if lvl is None:
            # heuristic guess
            lvl = int(math.log1p(min(rect[2], rect[3])) / math.log(self.MODE) + 0.5)
        elif lvl < 0:
            raise ValueError(f'lvl must be >= 0 or None, not {lvl}')

        if bucket < 1:
            raise ValueError(f'bucket must be >= 1, not {bucket}')

        self.rect = rect
        self.lvl = lvl
        self.bucket = bucket

        self.points = set()
        self.subtrees = None

    def __repr__(self):
        name = type(self).__qualname__
        return f"{name}({self.rect}, {self.lvl}, {self.bucket})"

    def __len__(self):
        if self.points is not None:
            return len(self.points)

        ln = 0
        for s in self.subtrees:
            ln += len(s)
        return ln

    def __bool__(self):
        return bool(self.subtrees) or bool(self.points)

    def _issizelimit(self):
        """Tests if tree is too small to be split into sub-trees.

        :return: True if size below minimum size, False if not.
        """
        return self.rect[2] < 3 or self.rect[3] < 3

    def _split(self):
        """Split tree into sub-trees."""
        # Calculation of rectangles for subtrees
        x, y, width, height = self.rect
        newlvl = self.lvl - 1

        # Sector layout
        # [0][1][2]
        # [3][4][5]
        # [6][7][8]

        # x0 = x
        # y0 = y
        w0 = width // 3
        h0 = height // 3

        x1 = x + w0  # x1 = x0 + w0
        # y1 = y0
        # w1 = w0
        # h1 = h0

        x2 = x + 2 * w0  # x2 = x0 + 2 * w0
        # y2 = y0
        w2 = width - 2 * w0
        # h2 = h0

        # x3 = x0
        y3 = y + h0  # y3 = y0 + h0
        # w3 = w0
        # h3 = h0

        # x4 = x1
        # y4 = y3
        # w4 = w0
        # h4 = h0

        # x5 = x2
        # y5 = y3
        # w5 = w2
        # h5 = h0

        # x6 = x0
        y6 = y + 2 * h0  # y6 = y0 + 2 * h0
        # w6 = w0
        h6 = height - 2 * h0

        # x7 = x1
        # y7 = y6
        # w7 = w0
        # h7 = h6

        # x8 = x2
        # y8 = y6
        # w8 = w2
        # h8 = h6

        self.subtrees = [NonTree((x, y, w0, h0), newlvl, self.bucket), NonTree((x1, y, w0, h0), newlvl, self.bucket),
                         NonTree((x2, y, w2, h0), newlvl, self.bucket), NonTree((x, y3, w0, h0), newlvl, self.bucket),
                         NonTree((x1, y3, w0, h0), newlvl, self.bucket), NonTree((x2, y3, w2, h0), newlvl, self.bucket),
                         NonTree((x, y6, w0, h6), newlvl, self.bucket), NonTree((x1, y6, w0, h6), newlvl, self.bucket),
                         NonTree((x2, y6, w2, h6), newlvl, self.bucket)]

    def _push_sub(self, point):
        """Push a point into a sub-tree.

        :param point: A data point in the shape of (x, y).
        """
        if point[0] < self.subtrees[1].rect[0]:  # x
            if point[1] < self.subtrees[3].rect[1]:  # y
                # push to upper left
                self.subtrees[0].add(point)
            elif point[1] < self.subtrees[6].rect[1]:  # y
                # push to upper middle
                self.subtrees[3].add(point)
            else:
                # push to upper right
                self.subtrees[6].add(point)
        elif point[0] < self.subtrees[2].rect[0]:  # x
            if point[1] < self.subtrees[3].rect[1]:  # y
                # push to middle left
                self.subtrees[1].add(point)
            elif point[1] < self.subtrees[6].rect[1]:  # y
                # push to middle middle
                self.subtrees[4].add(point)
            else:
                # push to middle right
                self.subtrees[7].add(point)
        else:
            if point[1] < self.subtrees[3].rect[1]:  # y
                # push to lower left
                self.subtrees[2].add(point)
            elif point[1] < self.subtrees[6].rect[1]:  # y
                # push to lower middle
                self.subtrees[5].add(point)
            else:
                # push to lower right
                self.subtrees[8].add(point)

    def add(self, point):
        """Adds a point to the tree.

        :param point: A point in the shape of (x, y).
        """
        if not self.subtrees and (len(self.points) < self.bucket or self.lvl == 0 or self._issizelimit()):
            self.points.add(point)
            return

        if not self.subtrees:  # leaf
            self._split()
            for p in self.points:
                self._push_sub(p)
            self.points = None

        self._push_sub(point)

    def discard(self, point):
        """Removes a point from the tree.

        :param point: A data point in the shape of (x, y).
        """
        if not self.subtrees:  # leaf
            self.points.discard(point)
            return

        for s in self.subtrees:
            if self.collide_rectpoint(s.rect, point):
                s.discard(point)
                return

    def get_encompassed(self):
        """Gets all points that are within the tree.

        :return: A list of points in the shape of (x, y).
        """
        if not self.subtrees:  # leaf
            return list(self.points)

        res = []
        for s in self.subtrees:
            res += s.get_encompassed()

        return res

    def get_rect(self, rect):
        """Gets all points that are within a rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :return: A list of points in the shape of (x, y).
        """
        if self.encompass_rectrect(rect, self.rect):
            return self.get_encompassed()

        if not self.subtrees:  # leaf
            return [p for p in self.points if self.collide_rectpoint(rect, p)]

        res = []
        for s in self.subtrees:
            if self.collide_rectrect(s.rect, rect):
                res += s.get_rect(rect)

        return res

    def get_circle(self, circ):
        """Gets all points that are within a circle.

        :param circ: A circle in the shape of (x, y, radius).
        :return: A list of points in the shape of (x, y).
        """
        if self.encompass_circlerect(circ, self.rect):
            return self.get_encompassed()

        if not self.subtrees:  # leaf
            return [p for p in self.points if self.collide_circlepoint(circ, p)]

        res = []
        for s in self.subtrees:
            if self.collide_rectcircle(s.rect, circ):
                res += s.get_circle(circ)

        return res

    def get_point(self, point):
        """Gets point if it is in the tree.

        :param point: A point in the shape of (x, y).
        :return: A list of point in the shape of (x, y).
        """
        if not self.subtrees:  # leaf
            if point in self.points:
                return [point]
        else:
            for s in self.subtrees:
                if self.collide_rectpoint(s.rect, point):
                    return s.get_point(point)

        return []

    def test_rect(self, rect):
        """Tests if there are points within a rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :return: True if there are points within the rectangle, False if not.
        """
        if not self.subtrees:  # leaf
            for p in self.points:
                if self.collide_rectpoint(rect, p):
                    return True
        else:
            for s in self.subtrees:
                if self.collide_rectrect(s.rect, rect):
                    if s.test_rect(rect):
                        return True

        return False

    def test_circle(self, circ):
        """Tests if there are points within a circle.

        :param circ: A circle in the shape of (x, y, radius).
        :return: True if there are points within the circle, False if not.
        """
        if not self.subtrees:  # leaf
            for p in self.points:
                if self.collide_circlepoint(circ, p):
                    return True
        else:
            for s in self.subtrees:
                if self.collide_rectcircle(s.rect, circ):
                    if s.test_circle(circ):
                        return True

        return False

    def test_point(self, point):
        """Tests if point is in the tree.

        :param point: A point in the shape of (x, y).
        :return: True if point is in the tree, False if not.
        """
        if not self.subtrees:  # leaf
            for p in self.points:
                if p == point:
                    return True
        else:
            for s in self.subtrees:
                if self.collide_rectpoint(s.rect, point):
                    if s.test_point(point):
                        return True
                    break

        return False

    def del_encompassed(self):
        """Deletes all points that are within the tree.

        :return: A list of deleted points.
        """
        if not self.subtrees:  # leaf
            deleted = list(self.points)
            self.points = set()
            return deleted

        deleted = []
        for s in self.subtrees:
            deleted += s.del_encompassed()
        return deleted

    def del_rect(self, rect):
        """Deletes points within a rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :return: A list of deleted points.
        """
        if self.encompass_rectrect(rect, self.rect):
            return self.del_encompassed()

        if not self.subtrees:  # leaf
            deleted = list(filter(lambda p: self.collide_rectpoint(rect, p), self.points))
            self.points.difference_update(deleted)
            return deleted

        deleted = []
        for s in self.subtrees:
            if self.collide_rectrect(s.rect, rect):
                deleted += s.del_rect(rect)
        return deleted

    def del_circle(self, circ):
        """Deletes points within a circle.

        :param circ: A circle in the shape of (x, y, radius).
        :return: A list of deleted points.
        """
        if self.encompass_circlerect(circ, self.rect):
            return self.del_encompassed()

        if not self.subtrees:  # leaf
            deleted = list(filter(lambda p: self.collide_circlepoint(circ, p), self.points))
            self.points.difference_update(deleted)
            return deleted

        deleted = []
        for s in self.subtrees:
            if self.collide_rectcircle(s.rect, circ):
                deleted += s.del_circle(circ)
        return deleted

    def del_point(self, point):
        """Deletes a point from the tree.

        :param point: A point in the shape of (x, y).
        :return: A list of deleted point.
        """
        if not self.subtrees:  # leaf
            try:
                self.points.remove(point)
            except KeyError:
                return []
            else:
                return [point]

        for s in self.subtrees:
            if self.collide_rectpoint(s.rect, point):
                return s.del_point(point)

    def prune(self):
        """Prunes empty sub-trees."""
        if not self.subtrees:  # leaf
            return

        for s in self.subtrees:
            s.prune()
            if s:  # s not empty
                return

        self.points = set()
        self.subtrees = None

    @staticmethod
    def encompass_rectrect(rect, other_rect):
        """Test if rectangle encompasses rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :param other_rect: A rectangle in shape of (x, y, width, height).
        :return: True if rect encompasses other_rect, False if not.
        """
        return rect[0] <= other_rect[0] and rect[1] <= other_rect[1] and rect[0] + rect[2] >= other_rect[0] + \
            other_rect[2] and rect[1] + rect[3] >= other_rect[1] + other_rect[3]

    @staticmethod
    def collide_rectpoint(rect, point):
        """Test collision between rectangle and point.

        :param rect: A rectangle in shape of (x, y, width, height).
        :param point: A point in the shape of (x, y).
        :return: True if collision, False if not.
        """
        return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]

    @staticmethod
    def collide_rectrect(rect, other_rect):
        """Test collision between rectangle and rectangle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :param other_rect: A rectangle in shape of (x, y, width, height).
        :return: True if collision, False if not.
        """
        return rect[0] < other_rect[0] + other_rect[2] and rect[1] < other_rect[1] + other_rect[3] and rect[0] + rect[
            2] > other_rect[0] and rect[1] + rect[3] > other_rect[1]

    @staticmethod
    @_conditional_njit
    def encompass_circlerect(circ, rect):
        """Test if circle encompasses rectangle.

        :param circ: A circle in the shape of (x, y, radius).
        :param rect: A rectangle in shape of (x, y, width, height).
        :return: True if circ encompasses rect, False if not.
        """
        dx = max(abs(circ[0] - rect[0]), abs(circ[0] - (rect[0] + rect[2])))
        dy = max(abs(circ[1] - rect[1]), abs(circ[1] - (rect[1] + rect[3])))

        return dx ** 2 + dy ** 2 <= circ[2] ** 2

    @staticmethod
    @_conditional_njit
    def collide_rectcircle(rect, circ):
        """Test collision between rectangle and circle.

        :param rect: A rectangle in shape of (x, y, width, height).
        :param circ: A circle in the shape of (x, y, radius).
        :return: True if collision, False if not.
        """
        dx = circ[0] - max(rect[0], min(circ[0], rect[0] + rect[2]))
        dy = circ[1] - max(rect[1], min(circ[1], rect[1] + rect[3]))

        return dx ** 2 + dy ** 2 <= circ[2] ** 2

    @staticmethod
    @_conditional_njit
    def collide_circlepoint(circ, point):
        """Test collision between circle and point.

        :param circ: A circle in the shape of (x, y, radius).
        :param point: A point in the shape of (x, y).
        :return: True if collision, False if not.
        """
        dx = circ[0] - point[0]
        dy = circ[1] - point[1]

        return dx ** 2 + dy ** 2 <= circ[2] ** 2
