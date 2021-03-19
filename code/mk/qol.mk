lint: $(VENV)
	. $(VENV) && cd public-schema-cli && black .
	. $(VENV) && cd public-schema-server && black .
	. $(VENV) && cd content-server && black .
	. $(VENV) && cd game-server && black .
	. $(VENV) && cd player-server && black .

.PHONY: lint