import numpy as np
import matplotlib.pyplot as plt


def naca4(m=4, p=4, t=12, n=200):

    m = m / 100
    p = p / 10
    t = t / 100

    x = np.linspace(0, 1, n)

    yt = (
        5
        * t
        * (
            0.2969 * np.sqrt(x)
            - 0.1260 * x
            - 0.3516 * x**2
            + 0.2843 * x**3
            - 0.1015 * x**4
        )
    )

    yc = np.where(
        x < p,
        m / (p**2) * (2 * p * x - x**2),
        m / ((1 - p) ** 2) * ((1 - 2 * p) + 2 * p * x - x**2),
    )

    dyc = np.where(
        x < p,
        2 * m / p**2 * (p - x),
        2 * m / (1 - p) ** 2 * (p - x),
    )

    theta = np.arctan(dyc)

    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)

    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    fig, ax = plt.subplots(figsize=(8,3))

    ax.plot(xu, yu, linewidth=2)
    ax.plot(xl, yl, linewidth=2)

    ax.fill_between(x, yu, yl, alpha=0.3)

    ax.set_aspect("equal")

    ax.set_title("Selected Airfoil")

    ax.axis("off")

    return fig