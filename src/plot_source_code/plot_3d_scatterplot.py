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


def main(
    kbq: BigQueryConnector, output_path: str = "/app/plots/3d_scatterplot.png"
) -> None:
    df = get_dataframe(kbq=kbq)

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
        df["_z_rating"],
        df["average_predicted_z_rating"],
        df["proof"],
        c=df["_cluster_label"],
        cmap="viridis",  # Better color palette (e.g., viridis, plasma, or rocket)
        s=500,  # Slightly smaller size for better clarity
        edgecolor="white",  # White border around points
        linewidth=0.6,
        alpha=0.8,  # Subtle transparency
    )

    # 3. Labels & Title
    # Added padding and font weights for readability
    ax.set_xlabel("Z-Score", labelpad=10, fontweight="bold")
    ax.set_ylabel("Avg Predicted Z-Score", labelpad=10, fontweight="bold")
    ax.set_zlabel("Alcohol by Volume", labelpad=10, fontweight="bold")
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


#####

if __name__ == "__main__":
    # Create connection to BigQuery
    kbq = BigQueryConnector("/app/src/service_accounts/ian_dev_v2.json")

    main(kbq=kbq, output_path="/app/plots/3d_scatterplot.png")
