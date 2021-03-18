PUBLIC_API_SERVER_DIR:=public-schema-server
PUBLIC_API_SERVER:=$(VENV)/bin/coal_public_api_server

$(PUBLIC_API_SERVER): $(GAME_SERVER)
	. $(VENV) && pip install -e $(PUBLIC_API_SERVER_DIR)


GAME_SERVER_DIR:=game-server
GAME_SERVER:=$(GAME_SERVER_DIR)/bin/coal_game_server

$(GAME_SERVER): $(VENV)
	. $(VENV) && pip install -e $(GAME_SERVER_DIR)


CONTENT_SERVER_DIR:=content-server
CONTENT_SERVER:=$(CONTENT_SERVER_DIR)/bin/coal_content_server

$(CONTENT_SERVER): $(VENV)
	. $(VENV) && pip install -e $(CONTENT_SERVER_DIR)

PLAYER_SERVER_DIR:=player-server
PLAYER_SERVER:=$(PLAYER_SERVER_DIR)/bin/coal_content_server

$(PLAYER_SERVER): $(VENV)
	. $(VENV) && pip install -e $(PLAYER_SERVER_DIR)


servers: $(PUBLIC_API_SERVER) $(GAME_SERVER) $(CONTENT_SERVER) $(PLAYER_SERVER)

clean::
	for i in build dist __pycache__ ; do \
		find $(PUBLIC_API_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; ; \
		find $(GAME_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; ; \
		find $(CONTENT_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; ; \
		find $(PLAYER_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; ; \
	done

.PHONY: servers clean