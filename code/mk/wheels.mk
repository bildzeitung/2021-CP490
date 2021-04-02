WHEEL_DIR:=$(abspath ./publish)

$(WHEEL_DIR):
	mkdir -p $@

wheels: $(VENV) build_number $(PUBLIC_API_SERVER_YAML) $(GAME_SERVER_YAML) $(CONTENT_SERVER_YAML) $(PLAYER_SERVER_YAML) | $(WHEEL_DIR)
	. $(VENV) && cd connexion && python -m build
	cp connexion/dist/*.whl $(WHEEL_DIR)
	for i in $(SERVER_MODS) ; do \
		echo "Building $${i}" ; \
		cd "$${i}" && echo "__version__ = \"$$(cat ../master-version.txt).$$(cat ../build-number.txt)\"" > "$$(ls -d coal_* | grep -v egg)/__version__.py"  && cd .. ; \
		. $(VENV) && cd "$${i}" && python -m build ; \
		cp dist/*.whl $(WHEEL_DIR) ; \
		git restore coal_*/__version__.py ; \
		cd .. ; \
	done

clean::
	rm -fr $(WHEEL_DIR)

.PHONY: wheels clean