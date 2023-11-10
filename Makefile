.PHONY: clean build dist upload

clean:
	rm -rf dist/
	rm -rf build/
	rm -rf k8s_namespace_viewer.egg-info/

build:
	python setup.py sdist bdist_wheel

check:
	twine check dist/*

upload:
	twine upload dist/*

dist: clean build check

all: clean build check upload

run_web:
	ttyd -p 8080 python -m kubestatus.viewer