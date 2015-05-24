.PHONY: clean-pyc clean-build docs

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "test-all - run tests on every Python version with tox"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "sdist - package"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 pubblicazioniASI

test:
	py.test

test-all:
	tox

docs:
	rm -f docs/.rst
	sphinx-apidoc -o docs/ pubblicazioniASI
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

sdist: clean
	python setup.py sdist
	ls -l dist

