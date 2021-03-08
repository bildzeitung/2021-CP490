VENV_DIR:=./venv
VENV:=$(VENV_DIR)/bin/activate

$(VENV_DIR):
	mkdir -p $@

$(VENV): requirements.txt | $(VENV_DIR)
	python -m venv $(VENV_DIR)
	. $@ && pip install --upgrade pip
	. $@ && pip install -r requirements.txt

virtualenv: $(VENV)

.PHONY: virtualenv