.PHONY: clean build dist upload

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf k8s_namespace_viewer.egg-info/

build:
	python setup.py sdist bdist_wheel

upload:
	twine upload dist/*

dist: clean build

all: clean build upload

run_web:
	ttyd -p 8080 python -m kubestatus.viewer