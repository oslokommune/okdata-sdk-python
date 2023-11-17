.PHONY: all
all: clean test bump-patch build publish-module

.PHONY: init
init:
	python3 -m pip install tox black pip-tools wheel twine bumpversion
	python3 -m piptools compile
	python3 -m pip install -rrequirements.txt

.PHONY: format
format:
	python3 -m black .

.PHONY: test
test:
	python3 -m tox -p auto

.PHONY: is-git-clean
is-git-clean:
	@status=$$(git fetch origin && git status -s -b) ;\
	if test "$${status}" != "## main...origin/main"; then \
		echo; \
		echo Git working directory is dirty, aborting >&2; \
		false; \
	fi

.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .tox

.PHONY: bump-patch
bump-patch: is-git-clean
	bumpversion patch

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

.PHONY: publish-module
publish-module:
	username=$$(op read op://Dataspeilet/pypi-upload-token/username) &&\
	password=$$(op read op://Dataspeilet/pypi-upload-token/credential) &&\
	python -m twine upload -u $$username -p $$password dist/*
