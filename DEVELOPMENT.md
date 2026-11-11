# Development

## Setup

Requirement: Python 3.11+

```sh
git clone git@github.com:oslokommune/okdata-sdk-python.git
cd okdata-sdk-python
make init
```

`make init` creates a virtual environment in `.build_venv` which the other
`make` targets install their tools into.

## Tests

`make test` runs the test suite with tox on every supported Python version,
along with flake8, black, and mypy:

```sh
make test
```

## Formatting

Reformat the code with black:

```sh
make format
```

## Upgrading dependencies

`requirements.txt` is generated with pip-tools. Upgrade every pinned
dependency with:

```sh
make upgrade-deps
```

## Making a new release

Make sure that `CHANGELOG.md` is up to date and committed to `main`, then run:

```sh
make bump-version-{patch,minor,major}
```

Use the `-patch`, `-minor`, or `-major` variant according to whether the new
release is a patch, minor, or major version respectively. This updates the
version in `setup.py` and `CHANGELOG.md`, commits the change, and tags the
commit with `v<version>`.

`make bump-version-*` and `make build` refuse to run unless the working tree is
clean and `main` is in sync with `origin/main`, so push the version bump commit
and the new tag before building:

```sh
git push
git push origin tag v<version>
```

Run `git tag -l` if you're unsure about the tag name.

### Uploading to PyPI

Releases are hosted at [PyPI](https://pypi.org/project/okdata-sdk/). Build the
new version with:

```sh
make build
```

This reformats the code, runs the tests, and builds a source distribution and a
wheel in `dist/`. Then upload them to PyPI with:

```sh
make publish
```

`make publish` reads the PyPI upload token from 1Password using the `op` CLI.

### Making a GitHub release

Go to https://github.com/oslokommune/okdata-sdk-python/tags and find the newly
pushed tag at the top of the list. Select the three dots (…), then "Create
release". Use the version as the title and the bullet points from `CHANGELOG.md`
as the description, following the format of previous releases.
