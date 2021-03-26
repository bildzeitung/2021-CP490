CLIENT:=public-schema-client
CLIENT_SETUP:=$(CLIENT)/setup.py

#
# OpenAPI tools
# - https://github.com/OpenAPITools/openapi-generator/blob/master/docs/generators/python.md
#
$(CLIENT_SETUP): $(PUBLIC_API_SERVER_YAML) $(VENV)
	docker run --rm -v "$$(pwd):/local" -u "$$(id -u):$$(id -g)" \
		openapitools/openapi-generator-cli \
		generate \
    --input-spec /local/public-schema-server/coal_public_api_server/openapi/openapi.yaml \
    --generator-name python \
    --output /local/public-schema-client \
		--additional-properties=packageName=coal_public_api_client
	. $(VENV) && pip install -e $(CLIENT)

COAL:=$(VENV_DIR)/bin/coal
$(COAL): $(CLIENT_SETUP)
	. $(VENV) && pip install -e ./public-schema-cli

client: $(COAL)

clean::
	rm -fr public-schema-client
	rm -fr public-schema-cli/coal.egg-info
	for i in build dist __pycache__ .tox ; do \
		find public-schema-cli -name "$${i}" -exec rm -fr {} \; || true ; \
	done

.PHONY: client