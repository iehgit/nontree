from NonTree import NonTree


class BiTree(NonTree):

    def __issizelimit(self):
        return self.rect[2] < 2

    def __push_sub(self, point):
        coord = point[0]

        if coord[0] < self.subtrees[1].rect[0]:  # x
            # push to left
            self.subtrees[0].push_point(point)
        else:
            # push to right
            self.subtrees[1].push_point(point)

    def __split(self):
        self.subtrees = []

        # Calculation of rectangles for subtrees
        x, y, width, height = self.rect
        newlvl = self.lvl - 1

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

        self.subtrees.append(BiTree((x, y, w0, height), newlvl))
        self.subtrees.append(BiTree((x1, y, w1, height), newlvl))
