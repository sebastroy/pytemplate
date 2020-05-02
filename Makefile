UNIT_DIR = test
TMP = build
VERSION := $(shell python3 setup.py --version)

.PHONY: all
all:

.PHONY: clean
clean:
	rm -rf $(TMP)

.PHONY: sdist
sdist:
	mkdir -p $(TMP)
	python3 setup.py sdist --dist-dir $(TMP) --manifest $(TMP)/MANIFEST

.PHONY: test
test: unit

.PHONY: unit
unit:
	python3 -munittest discover -s $(UNIT_DIR) $(TESTOPTS)

.PHONY: upload
upload: unit
	python3 setup.py sdist --dist-dir $(TMP) --manifest $(TMP)/MANIFEST upload
