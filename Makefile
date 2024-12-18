shell:
	@if [ ! -z $(build) ]; then				\
		docker compose up --build -d;		\
	else									\
		docker compose up -d;				\
	fi
	@docker compose exec -it whiskey_ml bash