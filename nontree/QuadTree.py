from NonTree import NonTree


class QuadTree(NonTree):

    def __issizelimit(self):
        return self.rect[2] < 2 or self.rect[3] < 2

    def __push_sub(self, point):
        coord = point[0]

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

    def __split(self):
        self.subtrees = []

        # Calculation of rectangles for subtrees
        x, y, width, height = self.rect
        newlvl = self.lvl - 1

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

        self.subtrees.append(QuadTree((x, y, w0, h0), newlvl))
        self.subtrees.append(QuadTree((x1, y, w1, h0), newlvl))
        self.subtrees.append(QuadTree((x, y2, w0, h2), newlvl))
        self.subtrees.append(QuadTree((x1, y2, w1, h2), newlvl))
