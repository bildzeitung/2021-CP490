lint: $(VENV)
	for i in $(SERVER_MODS) ; do \
		. $(VENV) && cd "$${i}" && black . && cd .. ; \
	done

.PHONY: lint