build:
	docker compose up --build -d

init_db:
	cd db/
	alembic upgrade head

stop:
	docker compose stop

clean:
	make stop
	docker compose --force
