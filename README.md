# infrBigDataLab4

commands:

- docker compose up --build --force-recreate
- docker compose up --build
- docker compose exec web-app bash -c "python -m unittest tests.tests"
- docker compose -f docker-compose-kafka.yml ps
- docker network create -d bridge broker-kafka