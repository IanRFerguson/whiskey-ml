from klondike import BigQueryConnector
from plot_3d_scatterplot import main as plot_3d_scatterplot_main

#####


def main(kbq: BigQueryConnector) -> None:
    plot_3d_scatterplot_main(kbq=kbq)


#####


if __name__ == "__main__":
    # Create connection to BigQuery
    kbq = BigQueryConnector("/app/src/service_accounts/ian_dev_v2.json")

    main(kbq=kbq)
