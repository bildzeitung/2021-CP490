PUBLIC_API_SERVER_DIR:=public-schema-server
PUBLIC_API_SERVER:=$(VENV)/bin/coal_public_api_server

$(PUBLIC_API_SERVER): $(GAME_SERVER)
	. $(VENV) && pip install -e $(PUBLIC_API_SERVER_DIR)


GAME_SERVER_DIR:=game-server
GAME_SERVER:=$(GAME_SERVER_DIR)/bin/coal_game_server

$(GAME_SERVER): $(VENV)
	. $(VENV) && pip install -e $(GAME_SERVER_DIR)


servers: $(PUBLIC_API_SERVER) $(GAME_SERVER)

clean::
	for i in "build dist" ; do \
		find $(PUBLIC_API_SERVER_DIR) -name "{$i}" -exec rm -fr {} \; ; \
		find $(GAME_SERVER_DIR) -name "${i}" -exec rm -fr {} \; ; \
	done

.PHONY: servers