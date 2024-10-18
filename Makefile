
## shortcuts
build:
	docker-compose build

stop:
	docker-compose stop

up:
	docker-compose up -d

launch:
	echo "Started building images"
	make build
	echo "Stop previous version containers"
	make stop
	echo "Launch new version containers"
	make up