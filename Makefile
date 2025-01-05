# Start interactive shell in Docker
shell:
	@if [ ! -z $(build) ]; then				\
		docker compose up --build -d;		\
	else									\
		docker compose up -d;				\
	fi
	@docker compose exec -it whiskey_ml bash


# Run dbt pipeline in Docker container and plot results
pipeline:
	@docker compose up -d
	@docker compose exec whiskey_ml dbt build -f
	@docker compose down
	@Rscript dev/plot_model_results.R