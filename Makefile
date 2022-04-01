help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
start:	## Start the docker container
	docker-compose up -d
bash:	## enter the docker container bash
	docker exec -it myaccountant_api-web-1 bash
stop:	## stop the docker containers
	docker-compose down
test:	## unittest the application using pytest
	@python -m pytest --cov=. tests/ --cov-report term --flake8
