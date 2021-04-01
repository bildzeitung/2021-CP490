#
# COAL ENGINE
#
include mk/venv.mk
include mk/server.mk
include mk/client.mk
include mk/qol.mk
include mk/build_number.mk
include mk/wheels.mk

all: client servers
	@echo "All done."

clean::
		find . -name 'dist' -exec rm -fr {} \;

realclean: clean
		rm -fr $(VENV_DIR)
		find . -name '*.db' -exec rm {} \;

undermud: $(VENV)
		. $(VENV) \
			&& coal_game_db_init \
		  && coal_content_db_init \
			&& coal_player_db_init \
			&& ./samples/undermud/loader.py

docker: wheels
	docker build . -t coal

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