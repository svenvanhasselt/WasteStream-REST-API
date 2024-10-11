all: build install

build:
	python3 setup.py sdist bdist_wheel

install:
	pip install .

run:
	python3 -m seenons_api.main

test:
	python3 -m pytest

clean:
	rm -rf build dist seenons_api.egg-info

.PHONY: all build install run test clean