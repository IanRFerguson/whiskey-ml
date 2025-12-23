# Start interactive shell in Docker
shell:
	@docker compose up --build -d;		
	@docker compose exec -it whiskey_ml bash


# Run dbt pipeline in Docker container and plot results
pipeline:
	@docker compose up -d
	@docker compose exec whiskey_ml dbt build -f
	@docker compose down
	@Rscript dev/plot_model_results.R


ruff:
	@ruff check . --fix
	@ruff format .


cluster-build:
	@gsutil cp ./devops/init_nltk.sh gs://whiskey-ml-dataproc-staging-bucket/init_nltk.sh
	@echo "Init script uploaded to GCS."
	@cd ./infra && terraform apply