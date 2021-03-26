PUBLIC_API_SERVER_DIR:=public-schema-server
GAME_SERVER_DIR:=game-server
CONTENT_SERVER_DIR:=content-server
PLAYER_SERVER_DIR:=player-server

# YAML directories
PUBLIC_API_SERVER_YAML_DIR:=$(PUBLIC_API_SERVER_DIR)/coal_public_api_server/openapi
PUBLIC_API_SERVER_YAML:=$(PUBLIC_API_SERVER_YAML_DIR)/openapi.yaml

GAME_SERVER_YAML_DIR:=$(GAME_SERVER_DIR)/coal_game_server/openapi
GAME_SERVER_YAML:=$(GAME_SERVER_YAML_DIR)/openapi.yaml

CONTENT_SERVER_YAML_DIR:=$(CONTENT_SERVER_DIR)/coal_content_server/openapi
CONTENT_SERVER_YAML:=$(CONTENT_SERVER_YAML_DIR)/openapi.yaml

PLAYER_SERVER_YAML_DIR:=$(PLAYER_SERVER_DIR)/coal_player_server/openapi
PLAYER_SERVER_YAML:=$(PLAYER_SERVER_YAML_DIR)/openapi.yaml

# YAML generation targets
$(PUBLIC_API_SERVER_YAML_DIR) $(GAME_SERVER_YAML_DIR) $(CONTENT_SERVER_DIR) $(PLAYER_SERVER_DIR):
	mkdir -p $@

$(PUBLIC_API_SERVER_YAML): | $(PUBLIC_API_SERVER_YAML_DIR)
	docker run \
		--rm \
		-v "$$(pwd):/local" \
		-u "$$(id -u):$$(id -g)" \
		swagger-cli bundle \
			--type yaml \
			--outfile /local/$(PUBLIC_API_SERVER_DIR)/coal_public_api_server/openapi/openapi.yaml \
			/local/openapi/public-schema.yaml

$(GAME_SERVER_YAML): | $(GAME_SERVER_YAML_DIR)
	docker run \
		--rm \
		-v "$$(pwd):/local" \
		-u "$$(id -u):$$(id -g)" \
		swagger-cli bundle \
			--type yaml \
			--outfile /local/$(GAME_SERVER_DIR)/coal_game_server/openapi/openapi.yaml \
			/local/openapi/game-server-schema.yaml

$(CONTENT_SERVER_YAML): | $(CONTENT_SERVER_YAML_DIR)
	docker run \
		--rm \
		-v "$$(pwd):/local" \
		-u "$$(id -u):$$(id -g)" \
		swagger-cli bundle \
			--type yaml \
			--outfile /local/$(CONTENT_SERVER_DIR)/coal_content_server/openapi/openapi.yaml \
			/local/openapi/content-server-schema.yaml

$(PLAYER_SERVER_YAML): | $(PLAYER_SERVER_YAML_DIR)
	docker run \
		--rm \
		-v "$$(pwd):/local" \
		-u "$$(id -u):$$(id -g)" \
		swagger-cli bundle \
			--type yaml \
			--outfile /local/$(PLAYER_SERVER_DIR)/coal_player_server/openapi/openapi.yaml \
			/local/openapi/player-server-schema.yaml

#
# Server targets
#
PUBLIC_API_SERVER:=$(VENV)/bin/coal_public_api_server

$(PUBLIC_API_SERVER): $(PUBLIC_API_SERVER_YAML) $(GAME_SERVER)
	. $(VENV) && pip install -e $(PUBLIC_API_SERVER_DIR)

GAME_SERVER:=$(GAME_SERVER_DIR)/bin/coal_game_server

$(GAME_SERVER): $(GAME_SERVER_YAML) $(VENV)
	. $(VENV) && pip install -e $(GAME_SERVER_DIR)

CONTENT_SERVER:=$(CONTENT_SERVER_DIR)/bin/coal_content_server

$(CONTENT_SERVER): $(CONTENT_SERVER_YAML) $(VENV)
	. $(VENV) && pip install -e $(CONTENT_SERVER_DIR)

PLAYER_SERVER:=$(PLAYER_SERVER_DIR)/bin/coal_content_server

$(PLAYER_SERVER): $(PLAYER_SERVER_YAML) $(VENV)
	. $(VENV) && pip install -e $(PLAYER_SERVER_DIR)

#
# PHONY targets
#
servers: $(PUBLIC_API_SERVER) $(GAME_SERVER) $(CONTENT_SERVER) $(PLAYER_SERVER)

yaml: $(PUBLIC_API_SERVER_YAML) $(GAME_SERVER_YAML) $(CONTENT_SERVER_YAML) $(PLAYER_SERVER_YAML)

clean::
	rm -f $(PUBLIC_API_SERVER_YAML) $(GAME_SERVER_YAML) $(CONTENT_SERVER_YAML) $(PLAYER_SERVER_YAML)
	for i in build dist __pycache__ .tox ; do \
		find $(PUBLIC_API_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; || true ; \
		find $(GAME_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; || true ; \
		find $(CONTENT_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; || true ; \
		find $(PLAYER_SERVER_DIR) -name "$${i}" -exec rm -fr {} \; || true ; \
	done
	rm -fr $(CONTENT_SERVER_DIR)/coal_content_server.egg-info
	rm -fr $(GAME_SERVER_DIR)/coal_game_server.egg-info
	rm -fr $(PLAYER_SERVER_DIR)/coal_player_server.egg-info
	rm -fr $(PUBLIC_API_SERVER_DIR)/coal_public_api_server.egg-info

.PHONY: servers yaml clean