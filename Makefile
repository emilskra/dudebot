build:
	docker compose up --build -d

migrate:
	cd db/
	alembic upgrade head

init_db:
	cd audio/
	python fill_data.py

stop:
	docker compose stop

clean:
	make stop
	docker compose --force
