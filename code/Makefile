#
# COAL ENGINE
#
include mk/vars.mk
include mk/venv.mk
include mk/server.mk
include mk/client.mk
include mk/qol.mk
include mk/build_number.mk
include mk/wheels.mk

all: client servers
	@echo "All done."

clean::
		find . -name 'dist' -exec rm -fr {} \; || true

realclean: clean
		rm -fr $(VENV_DIR)
		find . -name '*.db' -exec rm {} \;

undermud: $(VENV)
		. $(VENV) \
			&& coal_game_db_init \
		  && coal_content_db_init \
			&& coal_player_db_init \
			&& ./samples/undermud/loader.py

docker: clean wheels
	docker build . -t bildzeitung/cp490:$$(cat master-version.txt build-number.txt | paste -sd.)
	docker save bildzeitung/cp490:$$(cat master-version.txt build-number.txt | paste -sd.) | gzip > coal_docker_$$(cat master-version.txt build-number.txt | paste -sd.).tar.gz
	docker tag bildzeitung/cp490:$$(cat master-version.txt build-number.txt | paste -sd.) coal:latest

run:
	mkdir -p dbs
	docker run --rm \
		-p 8000:8000 \
		-v $$(pwd)/dbs:/data \
		-u "$$(id -u):$$(id -g)" \
		coal

newdb:
	find . -name '*.db' -exec rm {} \; ; coal_player_db_init ; coal_game_db_init ; coal_content_db_init

.PHONY: all clean realclean undermud run docker newdb

.DEFAULT_GOAL:= all