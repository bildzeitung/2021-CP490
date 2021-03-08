CLIENT:=coal_public_api_client
CLIENT_TOML:=$(CLIENT)/pyproject.toml

$(CLIENT_TOML): $(VENV)
	. $(VENV) && openapi-python-client --config ./public-schema/config.yaml generate --path ./public-schema/openapi.yaml --meta setup
	. $(VENV) && pip install -e $(CLIENT)


COAL:=$(VENV_DIR)/bin/coal
$(COAL): $(CLIENT_TOML)
	. $(VENV) && pip install -e ./public-schema-cli

client: $(COAL)

.PHONY: client