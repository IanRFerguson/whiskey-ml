# Start interactive shell in Docker
shell:
	@docker compose up whiskey_ml --build -d;		
	@docker compose exec -it whiskey_ml bash


# Run dbt pipeline in Docker container and plot results
pipeline:
	@docker compose up whiskey_ml -d
	@make dbt
	@make plots
	@docker compose down

dbt:
	@docker compose exec whiskey_ml bash -c "cd analytics && dbt build -f"

all-plots:
	@docker compose exec whiskey_ml python3 plot_source_code/run_all_plots.py


ruff:
	@ruff check . --fix
	@ruff format .


cluster-build:
	@gsutil cp ./devops/init_nltk.sh gs://whiskey-ml-dataproc-staging-bucket/init_nltk.sh
	@echo "Init script uploaded to GCS."
	@cd ./infra && terraform apply


docker-build:
	@gcloud auth configure-docker us-central1-docker.pkg.dev
	@docker build -f ./devops/Dockerfile.dataproc \
		--platform linux/amd64 \
		-t us-central1-docker.pkg.dev/ian-dev-444015/whiskey-ml/whiskey_ml_dataproc:latest \
		.
	@docker push us-central1-docker.pkg.dev/ian-dev-444015/whiskey-ml/whiskey_ml_dataproc:latest
	
	
docker-debugger:
	@docker compose up debugger --build -d;		
	@docker compose exec -it debugger bash