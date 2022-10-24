from NonTree import NonTree


class BiTree(NonTree):
    """A class for efficient collision detection of data points in a sparse 2D plane.
    Based on the well known Quadtree data structure.
    This is a variant that splits each plane into 2 sub-trees in a 1 by 2 grid.
    """

    MODE = 2

    def _issizelimit(self):
        """Tests if tree is too small to be split into sub-trees.

        :return: True if size below mimimum size, False if not.
        """
        return self.rect[2] < 2

    def _push_sub(self, data_point):
        """Push a data point into a sub-tree.

        :param data_point: A data point in the form of ((x,y), value).
        """
        point = data_point[0]

        if self.rect[3] > self.rect[2]:
            if point[1] < self.subtrees[1].rect[1]:  # y
                # push to upper
                self.subtrees[0].add(data_point)
            else:
                # push to lower
                self.subtrees[1].add(data_point)
        else:
            if point[0] < self.subtrees[1].rect[0]:  # x
                # push to left
                self.subtrees[0].add(data_point)
            else:
                # push to right
                self.subtrees[1].add(data_point)

    def _split(self):
        """Split tree into sub-trees.
        """
        self.subtrees = []

        # Calculation of rectangles for subtrees
        x, y, width, height = self.rect
        newlvl = self.lvl - 1

        if height > width:
            # Sector layout
            # [0]
            # [1]

            # x0 = x
            # y0 = y
            # w0 = width
            h0 = height // 2

            # x1 = x0
            y1 = y + h0  # y1 = y0 + h0
            # w1 = w0
            h1 = height - h0
            self.subtrees.append(BiTree((x, y, width, h0), newlvl))
            self.subtrees.append(BiTree((x, y1, width, h1), newlvl))
        else:
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
