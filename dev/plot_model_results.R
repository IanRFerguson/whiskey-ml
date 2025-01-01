library(tidyverse)
library(bigrquery)
library(ggplot2)
library(wesanderson)

#####

# Set local env and authenticate
setwd("/Users/Ian/Documents/GitHub/just-for-fun/2024/whiskey-ml/")
bq_auth("./src/service_accounts/ian_dev_v2.json")

# Load analytics table into memory
analytics <- bq_table_download("ian-dev-444015.dbt_analytics.prd__clean") %>% drop_na()

# Plot scatter plot of modeled vs. actual whiskey ratings
print("Plotting results of regression model...")
ml_plot <- analytics %>% 
                ggplot(
                        aes(
                                x=rating,
                                y=average_predicted_rating,
                                color=standard_styles
                        )
                ) +
                geom_point(
                        size=(analytics$proof / 3.85), 
                        alpha=0.55
                ) +
                labs(
                        x = "Actual Rating",
                        y = "Predicted Rating",
                        color = ""
                ) +
                scale_color_manual(
                        values=wes_palette(
                                n=4, 
                                name="Darjeeling1"
                        )
                ) +
                theme_classic()

# Save locally
ggsave(
        filename = "./plots/lr_results.png",
        width = 7.5,
        height = 7
)
print("Successfully saved plot")
