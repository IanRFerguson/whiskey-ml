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

### 01: Plot scatter plot of modeled vs. actual whiskey ratings
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
                        size=12, 
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

ggsave(
        filename = "./plots/lr_results.png",
        width = 8.5,
        height = 7
)


### 02: Plot individual prediction ranges
features <- c(
        'profile_id', 
        'standard_styles',
        'rating', 
        'minimum_predicted_rating', 
        'average_predicted_rating', 
        'maximum_predicted_rating',
        'actual_vs_predicted'
)
long.analytics <- analytics %>% 
                        select(all_of(features)) %>% 
                        arrange(profile_id) %>%
                        pivot_longer(
                                cols = -c(profile_id, standard_styles),
                                names_to = "rating_type"
                        ) %>% 
                        mutate(
                                is_predicted_value = str_detect(rating_type, "_predicted_"),
                                profile = as.factor(profile_id)
                        )

prediction.variance <- long.analytics %>% 
                        filter(is_predicted_value) %>% 
                        ggplot(
                                aes(
                                        x=profile, 
                                        y=value, 
                                        group=profile, 
                                        fill=standard_styles
                                )
                        ) +
                        geom_boxplot(
                                alpha=0.75, 
                                coef=0, 
                                outlier.shape = NA,
                                color='black'
                        ) +
                        scale_fill_manual(
                                values=wes_palette(
                                        n=4, 
                                        name="Darjeeling1"
                                )
                        ) +
                        labs(
                                x = "Whiskey Sample",
                                y = "Predicted Rating Variance",
                                fill = ""
                        ) +
                        theme_classic()

ggsave(
        filename = "./plots/model_ranges.png",
        width = 10,
        height = 7
)


### 03: Modeling categories
pred.categories <- analytics %>% 
                        select(c(standard_styles, actual_vs_predicted)) %>% 
                        ggplot(
                                aes(
                                        y=standard_styles, 
                                        x=actual_vs_predicted, 
                                        group=standard_styles, 
                                        fill=standard_styles
                                )
                        ) +
                        geom_vline(
                                xintercept=0,
                                linetype='dashed'
                        ) +
                        scale_fill_manual(
                                values=wes_palette(
                                        n=4, 
                                        name="Darjeeling1"
                                )
                        ) +
                        geom_boxplot(alpha=0.75) +
                        labs(
                                y = "",
                                x = "(Actual - Average Predicted Rating)",
                                fill = ""
                        ) +
                        theme_classic()

ggsave(
        filename = "./plots/model_categories.png",
        width = 10,
        height = 7
)
