import math


class NonTree:
    """A class for efficient collision detection of data points in a sparse 2D plane.
    Based on the well known Quadtree data structure.
    This is a variant that splits each plane into 9 sub-trees in a 3 by 3 grid.
    """

    MODE = 9

    def __init__(self, rect, lvl=None):
        """
        :param rect: A rectangle in form of (x, y, width, height).
        :param lvl: Maximum nesting depth. None for automatic heuristic value.
        """
        if lvl is None:
            # heuristic guess
            lvl = int(math.log(min(rect[2], rect[3])) // math.log(self.MODE))
        elif lvl < 0:
            raise ValueError(f'lvl must be >= 0 or None, not {lvl}')

        self.rect = rect
        self.lvl = lvl

        self.data_points = set()
        self.subtrees = None

    def __repr__(self):
        return f"{type(self).__qualname__}({self.rect}, {self.lvl})"

    def __len__(self):
        if self.data_points is not None:
            return len(self.data_points)

        ln = 0
        for s in self.subtrees:
            ln += len(s)
        return ln

    def __bool__(self):
        return self.subtrees or self.data_points

    def is_empty(self):
        """Test if the tree contains no values.

        :return: True if the tree contains no data points, False if not.
        """
        return not self.subtrees and not self.data_points

    def get_from_rect(self, rect):
        """Gets all data points that are within an rectangle.

        :param rect: A rectangle in form of (x, y, width, height).
        :return: A set of data points in the form of ((x, y), value).
        """
        if not self.subtrees:  # leaf
            return {dp for dp in self.data_points if self.collide_rectpoint(rect, dp[0])}

        res = set()
        for s in self.subtrees:
            if self.collide_rectrect(s.rect, rect):
                res |= s.get_from_rect(rect)

        return res

    def get_from_point(self, point):
        """Gets all data points that are on a point.

        :param point: A point in the form (x, y).
        :return: A set of data points in the form of ((x, y), value).
        """
        if not self.subtrees:  # leaf
            return {dp for dp in self.data_points if dp[0] == point}

        for s in self.subtrees:
            if self.collide_rectpoint(s.rect, point):
                return s.get_from_point(point)

        return set()

    def get_from_circle(self, circ):
        """Gets all data points that are within a circle.

        :param circ: A circle in the form (x, y, radius).
        :return: A set of data points in the form of ((x, y), value).
        """
        if not self.subtrees:  # leaf
            return {dp for dp in self.data_points if self.collide_circlepoint(circ, dp[0])}

        res = set()
        for s in self.subtrees:
            if self.collide_rectcircle(s.rect, circ):
                res |= s.get_from_circle(circ)

        return res

    def test_from_rect(self, rect):
        """Tests if there are data points within a rectangle.

        :param rect: A rectangle in form of (x, y, width, height).
        :return: True if there are data points within the rectangle, False if not.
        """
        if not self.subtrees:  # leaf
            for dp in self.data_points:
                if self.collide_rectpoint(rect, dp[0]):
                    return True
        else:
            for s in self.subtrees:
                if self.collide_rectrect(s.rect, rect):
                    if s.test_from_rect(rect):
                        return True

        return False

    def test_from_point(self, point):
        """Tests if there are data points on a point.

        :param point: A point in the form (x, y).
        :return: True if there are data points on the point, False if not.
        """
        if not self.subtrees:  # leaf
            for dp in self.data_points:
                if dp[0] == point:
                    return True
        else:
            for s in self.subtrees:
                if self.collide_rectpoint(s.rect, point):
                    if s.test_from_point(point):
                        return True
                    break

        return False

    def test_from_circle(self, circ):
        """Tests if there are data points within a circle.

        :param circ: A circle in the form (x, y, radius).
        :return: True if there are data points within the circle, False if not
        """
        if not self.subtrees:  # leaf
            for dp in self.data_points:
                if self.collide_circlepoint(circ, dp[0]):
                    return True
        else:
            for s in self.subtrees:
                if self.collide_rectcircle(s.rect, circ):
                    if s.test_from_circle(circ):
                        return True

        return False

    def del_from_rect(self, rect):
        """Deletes data points within a rectangle.

        :param rect: A rectangle in form of (x, y, width, height).
        """
        if not self.subtrees:  # leaf
            self.data_points = set(filter(lambda dp: not self.collide_rectpoint(rect, dp[0]), self.data_points))
            return

        for s in self.subtrees:
            if self.collide_rectrect(s.rect, rect):
                s.del_from_rect(rect)

    def del_from_point(self, point):
        """Deletes data points within on a point.

        :param point: A point in the form (x, y).
        """
        if not self.subtrees:  # leaf
            self.data_points = set(filter(lambda dp: dp[0] != point, self.data_points))
            return

        for s in self.subtrees:
            if self.collide_rectpoint(s.rect, point):
                s.del_from_point(point)
                break

    def del_from_circle(self, circ):
        """Deletes data points within a circle.

        :param circ: A circle in the form (x, y, radius).
        """
        if not self.subtrees:  # leaf
            self.data_points = set(filter(lambda dp: not self.collide_circlepoint(circ, dp[0]), self.data_points))
            return

        for s in self.subtrees:
            if self.collide_rectcircle(s.rect, circ):
                s.del_from_circle(circ)

    def prune(self):
        """Prunes empty sub-trees.
        """
        if not self.subtrees:  # leaf
            return

        all_empty = True
        for s in self.subtrees:
            s.prune()
            if not s.is_empty():
                all_empty = False
                break

        if all_empty:
            self.data_points = set()
            self.subtrees = None

    def _issizelimit(self):
        """Tests if tree is too small to be split into sub-trees.

        :return: True if size below mimimum size, False if not.
        """
        return self.rect[2] < 3 or self.rect[3] < 3

    def add_all(self, data_points):
        """Adds an iterable of data points to the tree.

        :param data_points: An iterable of data points in the form of ((x,y), value).
        """
        for data_point in data_points:
            self.add(data_point)

    def add_at(self, point, value):
        """Combines a point and data to a data point and adds it to the tree.

        :param point: A point in the form (x, y).
        :param value: Any data.
        """
        self.add((point, value))

    def add(self, data_point):
        """Adds a data point to the tree.

        :param data_point: A data point in the form of ((x,y), value).
        """
        if self.is_empty() or self.lvl == 0 or self._issizelimit():
            self.data_points.add(data_point)
            return  # value set

        if not self.subtrees:  # leaf
            self._split()
            for p in self.data_points:
                self._push_sub(p)
            self.data_points = None

        self._push_sub(data_point)

    def _push_sub(self, data_point):
        """Push a data point into a sub-tree.

        :param data_point: A data point in the form of ((x,y), value).
        """
        point = data_point[0]

        if point[0] < self.subtrees[1].rect[0]:  # x
            if point[1] < self.subtrees[3].rect[1]:  # y
                # push to upper left
                self.subtrees[0].add(data_point)
            elif point[1] < self.subtrees[6].rect[1]:  # y
                # push to upper middle
                self.subtrees[3].add(data_point)
            else:
                # push to upper right
                self.subtrees[6].add(data_point)
        elif point[0] < self.subtrees[2].rect[0]:  # x
            if point[1] < self.subtrees[3].rect[1]:  # y
                # push to middle left
                self.subtrees[1].add(data_point)
            elif point[1] < self.subtrees[6].rect[1]:  # y
                # push to middle middle
                self.subtrees[4].add(data_point)
            else:
                # push to middle right
                self.subtrees[7].add(data_point)
        else:
            if point[1] < self.subtrees[3].rect[1]:  # y
                # push to lower left
                self.subtrees[2].add(data_point)
            elif point[1] < self.subtrees[6].rect[1]:  # y
                # push to lower middle
                self.subtrees[5].add(data_point)
            else:
                # push to lower right
                self.subtrees[8].add(data_point)

    def _split(self):
        """Split tree into sub-trees.
        """
        self.subtrees = []

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

        self.subtrees.append(NonTree((x, y, w0, h0), newlvl))
        self.subtrees.append(NonTree((x1, y, w0, h0), newlvl))
        self.subtrees.append(NonTree((x2, y, w2, h0), newlvl))
        self.subtrees.append(NonTree((x, y3, w0, h0), newlvl))
        self.subtrees.append(NonTree((x1, y3, w0, h0), newlvl))
        self.subtrees.append(NonTree((x2, y3, w2, h0), newlvl))
        self.subtrees.append(NonTree((x, y6, w0, h6), newlvl))
        self.subtrees.append(NonTree((x1, y6, w0, h6), newlvl))
        self.subtrees.append(NonTree((x2, y6, w2, h6), newlvl))

    @staticmethod
    def collide_rectpoint(rect, point):
        """Test collision between rectangle and point.

        :param rect: A rectangle in form of (x, y, width, height).
        :param point: A point in the form (x, y).
        :return: True if collision, False if not.
        """
        return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]

    @staticmethod
    def collide_rectrect(rect, other_rect):
        """Test collision between rectangle and rectangle.

        :param rect: A rectangle in form of (x, y, width, height).
        :param other_rect: A rectangle in form of (x, y, width, height).
        :return: True if collision, False if not.
        """
        return rect[0] < other_rect[0] + other_rect[2] and rect[1] < other_rect[1] + other_rect[3] and rect[0] + rect[
            2] > other_rect[0] and rect[1] + rect[3] > other_rect[1]

    @staticmethod
    def collide_rectcircle(rect, circ):
        """Test collision between rectangle and circle.

        :param rect: A rectangle in form of (x, y, width, height).
        :param circ: A circle in the form (x, y, radius).
        :return: True if collision, False if not.
        """
        if not (NonTree.collide_rectrect(rect, (circ[0] - circ[2], circ[1] - circ[2], circ[2] * 2, circ[2] * 2))):
            return False

        if NonTree.collide_rectpoint(rect, circ):
            return True

        dx = circ[0] - max(rect[0], min(circ[0], rect[0] + rect[2]))
        dy = circ[1] - max(rect[1], min(circ[1], rect[1] + rect[3]))

        return dx ** 2 + dy ** 2 <= circ[2] ** 2

    @staticmethod
    def collide_circlepoint(circ, point):
        """Test collision between circle and point.

        :param circ: A circle in the form (x, y, radius).
        :param point: A point in the form (x, y).
        :return: True if collision, False if not.
        """
        dx = circ[0] - point[0]
        dy = circ[1] - point[1]

        return dx ** 2 + dy ** 2 <= circ[2] ** 2
