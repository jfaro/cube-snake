import matplotlib.pyplot as plt

from solver import Component, Configuration


def render_configuration(config: Configuration):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    for i in range(len(config.route) - 1):
        beg: Component = config.route[i]
        end: Component = config.route[i + 1]
        ax.plot(
            [beg.pos.x, end.pos.x],
            [beg.pos.y, end.pos.y],
            zs=[beg.pos.z, end.pos.z],
        )
    plt.show()
