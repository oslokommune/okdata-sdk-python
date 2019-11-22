import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="origo-sdk-python",
    version="0.0.1",
    author="Oslo Origo",
    author_email="dataplattform@oslo.kommune.no",
    description="SDK for origo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.oslo.kommune.no/origo-dataplatform/origo-sdk-python",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests",
        "urllib3",
        "PrettyTable",
        "python-keycloak-client",
        "PyJWT",
    ],
)
