from matplotlib import pyplot


def plot(ntree):
    """Plots the layout of a NonTree (or derivative) with mathplotlib

    :param ntree: A NonTree (or derivative)
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
    pyplot.show()
