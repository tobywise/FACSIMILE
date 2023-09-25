import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import r2_score
import numpy as np
from numpy.typing import ArrayLike
from typing import List
import pandas as pd


def plot_predictions(
    true: ArrayLike,
    pred: ArrayLike,
    factor_names: List[str] = None,
    scale: float = 1.0,
    fname: str = None,
    palette: List[str] = None,
):
    """
    Plot predicted factor scores against true factor scores.

    Args:
        true (ArrayLike): True factor scores.
        pred (ArrayLike): Predicted factor scores.
        factor_names (List[str], optional): List of factor names. Defaults to None.
        scale (float, optional): Scale of the plot. Defaults to 1.0.
        fname (str, optional): Filename to save the plot to. Defaults to None.
        palette (List[str], optional): List of colours to use for each factor. Defaults to None.
    """

    # Get number of factors
    n_factors = true.shape[1]

    # Make sure true and pred are numpy arrays
    true = np.array(true)
    pred = np.array(pred)

    # Check factor names are correct length
    if factor_names is not None:
        assert (
            len(factor_names) == n_factors
        ), "Number of factor names must equal number of factors"
    else:
        factor_names = ["Factor {}".format(i + 1) for i in range(n_factors)]

    # Set up figure
    f, ax = plt.subplots(
        1,
        n_factors,
        figsize=((n_factors * 3.333) * scale, 3.5 * scale),
        dpi=100,
        facecolor="white",
    )

    # If no palette is provided, use matplotlib default
    if palette is None:
        palette = [
            matplotlib.colors.to_hex(c)
            for c in plt.rcParams["axes.prop_cycle"].by_key()["color"]
        ]

    # If true is provided as a dataframe, convert to array
    if isinstance(true, pd.DataFrame):
        true = true.values

    # Plot each factor
    for i in range(n_factors):
        ax[i].scatter(x=true[:, i], y=pred[:, i], color=palette[i], alpha=0.2, s=0.5)
        ax[i].set_title(
            factor_names[i]
            + "\n$R^2$ = {0}".format(np.round(r2_score(true[:, i], pred[:, i]), 3)),
            fontweight="light",
        )

        # Add regression line
        ax[i].plot(
            np.unique(true[:, i]),
            np.poly1d(np.polyfit(true[:, i], pred[:, i], 1))(np.unique(true[:, i])),
            color=palette[i],
        )

        ax[i].set_xlabel("True score")
        ax[i].set_ylabel("Predicted score")
        ax[i].axis([-4, 4, -4, 4])
        (diag_line,) = ax[i].plot(
            ax[i].get_xlim(), ax[i].get_ylim(), ls="--", color=palette[i]
        )

    plt.tight_layout()

    if fname is not None:
        plt.savefig(fname, dpi=300)

    plt.show()
