class NonTree:

    def __init__(self, rect, mode, use_sets=False):
        if mode not in (2, 4, 9):
            raise ValueError(f'mode must be in(2, 4, 9), not {mode}')

        self.rect = rect  # (x, y, width, height)
        self.mode = mode
        self.use_sets = use_sets

        self.coord = None
        if self.use_sets:
            self.value = set()
        else:
            self.value = None

        self.subtrees = []

    def is_leaf(self):
        return len(self.subtrees) == 0

    def is_empty(self):
        if not self.is_leaf():
            return False

        return self.coord is None

    def get_from_rect(self, rect):
        pass  # TODO

    def get_from_coord(self, coord):
        pass  # TODO

    def del_from_rect(self, rect):
        pass  # TODO

    def del_from_coord(self, coord):
        pass  # TODO

    def push_all(self, coord_values):
        for coord_value in coord_values:  # coord_value: ((x,y), value)
            coord, value = coord_value
            self.push(coord, value)

    def push(self, coord, value):  # coord: (x,y)
        if self.is_empty():
            self.coord = coord
            if self.use_sets:
                self.value.add(value)
            else:
                self.value = value
            return  # value set

        if self.is_leaf() and coord == self.coord:
            if self.use_sets:
                self.value.add(value)
            else:
                self.value = value
            return  # value updated

        if self.is_leaf():
            self.__split()
            self.__push_sub(self.coord, self.value)
            self.coord = None
            if self.use_sets:
                self.value.clear()
            else:
                self.value = None

        self.__push_sub(coord, value)

    def __push_sub(self, coord, value):
        if self.mode == 2:
            if coord[0] < self.subtrees[1].rect[0]:  # x
                # push to left
                self.subtrees[0].push(coord, value)
            else:
                # push to right
                self.subtrees[1].push(coord, value)

        elif self.mode == 4:
            if coord[0] < self.subtrees[1].rect[0]:  # x
                if coord[1] < self.subtrees[2].rect[1]:  # y:
                    # push to upper left
                    self.subtrees[0].push(coord, value)
                else:
                    # push to lower left
                    self.subtrees[2].push(coord, value)
            else:
                if coord[1] < self.subtrees[3].rect[1]:  # y:
                    # push to upper right
                    self.subtrees[1].push(coord, value)
                else:
                    # push to lower right
                    self.subtrees[3].push(coord, value)

        elif self.mode == 9:
            pass  # TODO

    def __split(self):  # add subtrees
        x, y, width, height = self.rect

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

            self.subtrees.append(NonTree((x, y, w0, height), self.mode, self.use_sets))
            self.subtrees.append(NonTree((x1, y, w1, height), self.mode, self.use_sets))

            pass  # TODO

        elif self.mode == 4:
            # Sector layout
            # [0][1]
            # [2][3]

            # Calculation of rectangles for subtrees

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

            self.subtrees.append(NonTree((x, y, w0, h0), self.mode, self.use_sets))
            self.subtrees.append(NonTree((x1, y, w1, h0), self.mode, self.use_sets))
            self.subtrees.append(NonTree((x, y2, w0, h2), self.mode, self.use_sets))
            self.subtrees.append(NonTree((x1, y2, w1, h2), self.mode, self.use_sets))

        elif self.mode == 9:
            # Sector layout
            # [0][1][2]
            # [3][4][5]
            # [6][7][8]
            pass  # TODO
