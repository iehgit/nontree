class NonTree:

    def __init__(self, rect, mode, lvl):
        if mode not in (2, 4, 9):
            raise ValueError(f'mode must be in(2, 4, 9), not {mode}')
        if lvl < 0:
            raise ValueError(f'lvl must be >= 0, not {lvl}')

        self.rect = rect  # (x, y, width, height)
        self.mode = mode
        self.lvl = lvl

        self.points = set()
        self.subtrees = []

    def is_leaf(self):
        return not self.subtrees

    def is_empty(self):
        return not self.subtrees and not self.points

    def get_from_rect(self, rect):
        if self.is_leaf():
            return [p for p in self.points if self.collidepoint(rect, p[0])]

        res = []
        for s in self.subtrees:
            if self.colliderect(s.rect, rect):
                res.extend(s.get_from_rect(rect))

        return res

    def get_from_coord(self, coord):
        if self.is_leaf():
            return [p for p in self.points if p[0] == coord]

        for s in self.subtrees:
            if self.collidepoint(s.rect, coord):
                return s.get_from_coord(coord)

        return []

    def test_from_rect(self, rect):
        if self.is_leaf():
            for p in self.points:
                if self.collidepoint(rect, p[0]):
                    return True

        for s in self.subtrees:
            if s.colliderect(s.rect, rect):
                if s.test_from_rect(rect):
                    return True

        return False

    def test_from_coord(self, coord):
        if self.is_leaf():
            for p in self.points:
                if p[0] == coord:
                    return True

        for s in self.subtrees:
            if s.collidepoint(s.rect, coord):
                if s.test_from_coord(coord):
                    return True
                break

        return False

    def del_from_rect(self, rect):
        if self.is_leaf():
            self.points = set(filter(lambda p: not self.collidepoint(rect, p[0]), self.points))
            return

        for s in self.subtrees:
            if self.colliderect(s.rect, rect):
                s.del_from_rect(rect)

    def del_from_coord(self, coord):
        if self.is_leaf():
            self.points = set(filter(lambda p: p[0] != coord, self.points))
            return

        for s in self.subtrees:
            if self.collidepoint(s.rect, coord):
                s.del_from_coord(coord)
                break

    def prune(self):
        if self.is_leaf():
            return

        all_empty = True
        for s in self.subtrees:
            s.prune()
            if not s.is_empty():
                all_empty = False
                break

        if all_empty:
            self.subtrees.clear()

    def __issizelimit(self):
        if self.mode == 2:
            return self.rect[2] < 2
        elif self.mode == 4:
            return self.rect[2] < 2 or self.rect[3] < 2
        elif self.mode == 9:
            return self.rect[2] < 3 or self.rect[3] < 3

    def push_points(self, points):
        for point in points:  # point: ((x,y), value)
            self.push_point(point)

    def push(self, coord, value):
        self.push_point((coord, value))

    def push_point(self, point):  # point: ((x,y), value)
        if self.is_empty() or self.lvl == 0 or self.__issizelimit():
            self.points.add(point)
            return  # value set

        if self.is_leaf():
            self.__split()
            for p in self.points:
                self.__push_sub(p)
            self.points.clear()

        self.__push_sub(point)

    def __push_sub(self, point):
        coord = point[0]

        if self.mode == 2:
            if coord[0] < self.subtrees[1].rect[0]:  # x
                # push to left
                self.subtrees[0].push_point(point)
            else:
                # push to right
                self.subtrees[1].push_point(point)

        elif self.mode == 4:
            if coord[0] < self.subtrees[1].rect[0]:  # x
                if coord[1] < self.subtrees[2].rect[1]:  # y
                    # push to upper left
                    self.subtrees[0].push_point(point)
                else:
                    # push to lower left
                    self.subtrees[2].push_point(point)
            else:
                if coord[1] < self.subtrees[2].rect[1]:  # y
                    # push to upper right
                    self.subtrees[1].push_point(point)
                else:
                    # push to lower right
                    self.subtrees[3].push_point(point)

        elif self.mode == 9:
            if coord[0] < self.subtrees[1].rect[0]:  # x
                if coord[1] < self.subtrees[3].rect[1]:  # y
                    # push to upper left
                    self.subtrees[0].push_point(point)
                elif coord[1] < self.subtrees[6].rect[1]:  # y
                    # push to upper middle
                    self.subtrees[3].push_point(point)
                else:
                    # push to upper right
                    self.subtrees[6].push_point(point)
            elif coord[0] < self.subtrees[2].rect[0]:  # x
                if coord[1] < self.subtrees[3].rect[1]:  # y
                    # push to middle left
                    self.subtrees[1].push_point(point)
                elif coord[1] < self.subtrees[6].rect[1]:  # y
                    # push to middle middle
                    self.subtrees[4].push_point(point)
                else:
                    # push to middle right
                    self.subtrees[7].push_point(point)
            else:
                if coord[1] < self.subtrees[3].rect[1]:  # y
                    # push to lower left
                    self.subtrees[2].push_point(point)
                elif coord[1] < self.subtrees[6].rect[1]:  # y
                    # push to lower middle
                    self.subtrees[5].push_point(point)
                else:
                    # push to lower right
                    self.subtrees[8].push_point(point)

    def __split(self):
        # Calculation of rectangles for subtrees
        x, y, width, height = self.rect
        newlvl = self.lvl - 1

        if self.mode == 2:
            # Sector layout
            # [0][1]

            # x0 = x
            # y0 = y
            w0 = width // 2
            # h0 = height

            x1 = x + w0  # x1 = x0 + w0
            # y1 = y0
            w1 = width - w0
            # h1 = h0

            self.subtrees.append(NonTree((x, y, w0, height), self.mode, newlvl))
            self.subtrees.append(NonTree((x1, y, w1, height), self.mode, newlvl))

        elif self.mode == 4:
            # Sector layout
            # [0][1]
            # [2][3]

            # x0 = x
            # y0 = y
            w0 = width // 2
            h0 = height // 2

            x1 = x + w0  # x1 = x0 + w0
            # y1 = y0
            w1 = width - w0
            # h1 = h0

            # x2 = x0
            y2 = y + h0  # y2 = y0 + h0
            # w2 = w0
            h2 = height - h0

            # x3 = x1
            # y3 = y2
            # w3 = w1
            # h3 = h2

            self.subtrees.append(NonTree((x, y, w0, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x1, y, w1, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x, y2, w0, h2), self.mode, newlvl))
            self.subtrees.append(NonTree((x1, y2, w1, h2), self.mode, newlvl))

        elif self.mode == 9:
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

            self.subtrees.append(NonTree((x, y, w0, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x1, y, w0, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x2, y, w2, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x, y3, w0, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x1, y3, w0, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x2, y3, w2, h0), self.mode, newlvl))
            self.subtrees.append(NonTree((x, y6, w0, h6), self.mode, newlvl))
            self.subtrees.append(NonTree((x1, y6, w0, h6), self.mode, newlvl))
            self.subtrees.append(NonTree((x2, y6, w2, h6), self.mode, newlvl))

    @staticmethod
    def collidepoint(rect, point):
        return rect[0] <= point[0] <= rect[0] + rect[2] and rect[1] <= point[1] <= rect[1] + rect[3]

    @staticmethod
    def colliderect(rect, other_rect):
        return rect[0] < other_rect[0] + other_rect[2] and rect[1] < other_rect[1] + other_rect[3] and rect[0] + rect[
            2] > other_rect[0] and rect[1] + rect[3] > other_rect[1]
