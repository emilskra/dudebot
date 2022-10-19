build:
	docker compose up --build -d

migrate:
	alembic upgrade head

make_migrations:
	cd migrations
	alembic revision --autogenerate -m "$(message)"

stamp_head:
	cd migrations
	alembic stamp head

init_db:
	cd audio/
	python fill_data.py

stop:
	docker compose stop

clean:
	make stop
	docker compose --force

.EXPORT_ALL_VARIABLES:
export PYTHONPATH := $(shell pwd)/src:$(PYTHONPATH)
