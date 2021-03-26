WHEEL_DIR:=./publish

$(WHEEL_DIR):
	mkdir -p $@

wheels: $(VENV) $(PUBLIC_API_SERVER_YAML) | $(WHEEL_DIR)
	. $(VENV) && cd public-schema-server && python -m build
	. $(VENV) && cd game-server && python -m build
	. $(VENV) && cd content-server && python -m build
	. $(VENV) && cd player-server && python -m build
	. $(VENV) && cd connexion && python -m build
	cp connexion/dist/*.whl $(WHEEL_DIR)
	cp public-schema-server/dist/coal_public_api_server-*.whl $(WHEEL_DIR)
	cp game-server/dist/coal_*.whl $(WHEEL_DIR)
	cp content-server/dist/coal_*.whl $(WHEEL_DIR)
	cp player-server/dist/coal_*.whl $(WHEEL_DIR)

.PHONY: wheels