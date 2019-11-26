.PHONY: all
all: clean test bump-patch build publish-module

.PHONY: init
init:
	python3 -m pip install tox black pip-tools wheel twine bumpversion
	pip-compile
	pip install -rrequirements.txt

.PHONY: format
format:
	python3 -m black .

.PHONY: test
test:
	python3 -m tox -p auto

.PHONY: is-git-clean
is-git-clean:
	@status=$$(git fetch origin && git status -s -b) ;\
	if test "$${status}" != "## master...origin/master"; then \
		echo; \
		echo Git working directory is dirty, aborting >&2; \
		false; \
	fi

.PHONY: clean
clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info


.PHONY: bump-patch
bump-patch:
	bumpversion patch
	git push

.PHONY: build
build:
	python3 setup.py sdist bdist_wheel

.PHONY: publish-module
publish-module:
	username=$$(gopass show dataplatform/websites/pypi.org/origo-dataplatform username) &&\
	password=$$(gopass show --password dataplatform/websites/pypi.org/origo-dataplatform) &&\
	python -m twine upload -u $$username -p $$password dist/*
