gen-cert:
	mkdir -p cert && \
	cd cert && \
	openssl req -x509 -newkey rsa:2048 -keyout keytmp.pem -out cert.pem -days 365 -nodes -subj "/emailAddress=dev@www.example.com" && \
	openssl rsa -in keytmp.pem -out key.pem

build_kong:
	docker-compose build kong

run_db:
	docker-compose up -d db

run_upstream:
	docker-compose build upstream
	docker-compose up -d upstream

migrate_kong:
	docker-compose run kong kong migrations bootstrap

run_kong:
	docker-compose run --rm -d --service-ports kong kong start