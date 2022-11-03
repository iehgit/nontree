from matplotlib import pyplot


def plot(ntree, overlay=None):
    """Plots the layout of a NonTree (or derivative) with matplotlib.
    Optionally plots an overlay of additional points on top, in a different color.

    :param ntree: A NonTree (or derivative)
    :param overlay: A list of points in the shape of (x, y).
    """

    pyplot.figure(figsize=(20, 20))
    pyplot.title(ntree)

    x = []
    y = []

    axes = pyplot.gca()

    def subplot(n):
        axes.add_patch(pyplot.Rectangle((n.rect[0], n.rect[1]), n.rect[2], n.rect[3], fill=False))

        if n.points:
            for p in n.points:
                x.append(p[0])
                y.append(p[1])

        if n.subtrees:
            for s in n.subtrees:
                subplot(s)

    subplot(ntree)
    pyplot.plot(x, y, 'r.')

    if overlay:
        x2 = []
        y2 = []
        for p2 in overlay:
            x2.append(p2[0])
            y2.append(p2[1])

        pyplot.plot(x2, y2, 'b.')

    pyplot.show()
