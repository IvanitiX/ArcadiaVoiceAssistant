all: up

deploy: pull build stop up

build:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache

up:
	docker-compose up -d

start:
	docker-compose start

stop:
	docker-compose stop

down:
	docker-compose down

down_remove_images:
	docker-compose down --rmi local

pull:
	git pull