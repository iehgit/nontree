from matplotlib import patches, pyplot


def plot(ntree):
    pyplot.figure(figsize=(20, 20))
    pyplot.title(f"{ntree.MODE}-tree")

    x = []
    y = []

    def subplot(n):
        pyplot.gca().add_patch(patches.Rectangle((n.rect[0], n.rect[1]), n.rect[2], n.rect[3], fill=False))

        if n.data_points:
            for dp in n.data_points:
                p = dp[0]
                x.append(p[0])
                y.append(p[1])

        if n.subtrees:
            for s in n.subtrees:
                subplot(s)

    subplot(ntree)
    pyplot.plot(x, y, 'r.')
    pyplot.show()
