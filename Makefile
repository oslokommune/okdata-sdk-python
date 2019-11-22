.PHONY: init
init:
	python3 -m pip install tox black pip-tools
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
