# Development

## Getting started

Setup
```
git clone git@github.com:oslokommune/okdata-sdk-python.git
cd okdata-sdk-python
python3.8 -m venv .venv
source .venv/bin/activate
make init
```

Run all tests:
```
$ make test
```

Reformat files:
```
make format
```

## Releasing a new SDK version
* Checkout the `main` branch
* Either run `make`

or manually run the make targets:
1. Test
```
make clean test
```
2. Bump version and build
```
make bump-patch build
```
3. Publish the module to PyPI
```
make publish-module
```
4. Push the version bump commit and the generated tag
  to GitHub.
```
git push
git push --tags
```
5. Create new release in github.
    1. Go to https://github.com/oslokommune/okdata-sdk-python/tags
    2. On the latest tag, click on `...` -> `Create release`
    3. Fill out `Title`-field with the new release version. Fill out `Write`-field with value (bullet points) from latest release in CHANGELOG
    4. Click `Publish release`
