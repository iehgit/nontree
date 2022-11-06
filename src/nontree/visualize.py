import random
from matplotlib import pyplot

from nontree.NonTree import NonTree


def plot(ntree, overlay=None, **kwargs):
    """Plots the layout of a NonTree (or derivative), using matplotlib.\x20\x20
    Optionally plots an overlay of additional points on top, in a different color.

    :param ntree: A NonTree (or derivative).
    :param overlay: A list of points in the shape of (x, y).
    :param kwargs: Keyword arguments, forwared to matplotlib.pyplot.figure().
    """
    pyplot.figure(**kwargs)
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


def plot_demo():
    """Plots the layout of a demo NonTree, using matplotlib.\x20\x20
    Also plots an overlay of additional points on top, in a different color."""
    ntree = NonTree((0, 0, 30000, 30000))
    for i in range(2200):
        x = random.randrange(30000)
        y = random.randrange(30000)
        if not (x < 5000 and y < 5000):
            ntree.add((x, y))

    for i in range(100):
        x = random.randrange(26500, 29000)
        y = random.randrange(26500, 29000)
        ntree.add((x, y))

    overlay = ntree.get_circle((15000, 15000, 10000))
    plot(ntree, overlay, figsize=(10, 10))


if __name__ == '__main__':
    plot_demo()
