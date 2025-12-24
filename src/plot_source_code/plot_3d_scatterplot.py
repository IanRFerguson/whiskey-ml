from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from klondike import BigQueryConnector

#####


def get_dataframe(
    kbq: BigQueryConnector, target_table: str = "dbt_analytics.prd__clean"
) -> pd.DataFrame:
    """
    Reads a BigQuery table into a Pandas DataFrame.
    """

    df = kbq.read_dataframe(f"SELECT * FROM {target_table}").to_pandas()

    return df


def write_plot_to_file(
    df: pd.DataFrame,
    output_path: str,
    x_var: str,
    y_var: str,
    z_var: str,
    label_var: str,
) -> None:
    """
    Generates a 3D scatter plot and saves it to a file.
    """

    # Use a clean theme
    sns.set_theme(style="whitegrid")

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection="3d")

    # 1. Aesthetics: Clean up the 3D Panes
    # We make the background planes a light grey and remove the grid lines for a cleaner look
    ax.xaxis.pane.set_facecolor((0.95, 0.95, 0.95, 1.0))
    ax.yaxis.pane.set_facecolor((0.95, 0.95, 0.95, 1.0))
    ax.zaxis.pane.set_facecolor((0.95, 0.95, 0.95, 1.0))
    ax.xaxis.pane.set_edgecolor("w")
    ax.yaxis.pane.set_edgecolor("w")
    ax.zaxis.pane.set_edgecolor("w")

    # 2. Scatter Plot: Improved markers and colors
    # - 'cmap' provides a professional color gradient
    # - 'edgecolor' makes points pop against each other
    # - 'alpha' helps visualize density where points overlap
    scatter = ax.scatter(
        df[x_var],
        df[y_var],
        df[z_var],
        c=df[label_var],
        cmap="viridis",  # Better color palette (e.g., viridis, plasma, or rocket)
        s=500,  # Slightly smaller size for better clarity
        edgecolor="white",  # White border around points
        linewidth=0.6,
        alpha=0.8,  # Subtle transparency
    )

    # 3. Labels & Title
    # Added padding and font weights for readability
    ax.set_xlabel(x_var, labelpad=10, fontweight="bold")
    ax.set_ylabel(y_var, labelpad=10, fontweight="bold")
    ax.set_zlabel(z_var, labelpad=10, fontweight="bold")
    plt.title(
        "Whiskey Analysis: Cluster Distribution", fontsize=16, pad=20, fontweight="bold"
    )

    # 4. Legend Fix
    # Using scatter.legend_elements() is the correct way to get a legend for a single scatter call
    ax.legend(
        *scatter.legend_elements(),
        loc="center left",
        title="Clusters",
        bbox_to_anchor=(1.05, 0.5),
    )

    # 5. Viewing Angle
    # Setting an initial angle often helps the user understand the 3D space immediately
    ax.view_init(elev=20, azim=135)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)


def main(kbq: BigQueryConnector) -> None:
    df = get_dataframe(kbq=kbq)
    write_plot_to_file(
        df=df,
        output_path=f"/app/plots/{datetime.now().strftime('%Y')}/3d_scatterplot__by_cluster.png",
        x_var="_z_rating",
        y_var="average_predicted_z_rating",
        z_var="semantic_score",
        label_var="cluster_label",
    )

    # write_plot_to_file(
    #     df=df,
    #     output_path="/app/3d_scatterplot__by_style.png",
    #     x_var="_z_rating",
    #     y_var="average_predicted_z_rating",
    #     z_var="semantic_score",
    #     label_var="standard_styles",
    # )


#####

if __name__ == "__main__":
    # Create connection to BigQuery
    kbq = BigQueryConnector("/app/src/service_accounts/ian_dev_v2.json")

    main(kbq=kbq)
