all: build install

build:
	python3 setup.py sdist bdist_wheel

install:
	pip install .

run:
	python3 -m seenons_api.main

clean:
	rm -rf build dist seenons_api.egg-info
	find . -name "__pycache__" -exec rm -r {} +

.PHONY: all build install run clean