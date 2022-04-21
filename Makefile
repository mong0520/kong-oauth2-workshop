gen-cert:
	mkdir -p cert && \
	cd cert && \
	openssl req -x509 -newkey rsa:2048 -keyout keytmp.pem -out cert.pem -days 365

gen-cert-key:
	cd cert && \
	openssl rsa -in keytmp.pem -out key.pem

build:
	docker-compose build kong

run_db:
	docker-compose up -d db

migrate:
	docker-compose run kong kong migrations bootstrap

run:
	docker-compose run --rm --service-ports kong kong start