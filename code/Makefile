#
# COAL ENGINE
#
include mk/venv.mk
include mk/client.mk
include mk/server.mk
include mk/qol.mk

all: client servers
	@echo "All done."

clean::
	rm -fr $(CLIENT)

realclean: clean
		rm -fr $(VENV_DIR)
		find . -name '*.db' -exec rm {} \;

undermud: $(VENV)
		. $(VENV) \
			&& coal_game_db_init \
		  && coal_content_db_init \
			&& coal_player_db_init \
			&& ./samples/undermud/loader.py


.PHONY: all clean realclean undermud

.DEFAULT_GOAL:= all