#
# COAL ENGINE
#
include mk/venv.mk
include mk/client.mk
include mk/server.mk

all: client servers
	@echo "All done."

clean::
	rm -fr $(CLIENT)

realclean: clean
		rm -fr $(VENV_DIR)
		find . -name '*.db' -exec rm {} \;



.PHONY: all clean realclean

.DEFAULT_GOAL:= all