PYTHON = env python
PACKAGE = pytemplate
LINT_HARD ?= false

ifeq ($(LINT_HARD), false)
	EXTRA_OPTIONS = --exit-zero
endif


.PHONY: lint
lint:
	$(PYTHON) -m pylint $(PACKAGE) $(EXTRA_OPTIONS)
	$(PYTHON) -m flake8

.PHONY: build
build: lint
	$(PYTHON) -m build

.PHONY: lint
clean:
	rm -rf dist *.egg-info __pycache__ */__pycache__
