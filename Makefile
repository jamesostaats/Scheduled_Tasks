build:
	docker-compose up -d --build base_dash

logs:
	docker-compose logs --tail 100 -f

restart:
	docker-compose restart