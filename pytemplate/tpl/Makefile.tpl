PYTHON = env python
PACKAGE = {library_name}
LINT_HARD ?= false

ifeq ($(LINT_HARD), false)
	EXTRA_OPTIONS = --exit-zero
endif


lint:
	$(PYTHON) -m pylint $(PACKAGE) $(EXTRA_OPTIONS)
	$(PYTHON) -m flake8

build: lint
	$(PYTHON) -m build

clean:
	rm -rf dist *.egg-info __pycache__ */__pycache__
