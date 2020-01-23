import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="origo-sdk-python",
    version="0.0.15",
    author="Oslo Origo",
    author_email="dataplattform@oslo.kommune.no",
    description="SDK for origo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/origo-sdk-python",
    packages=setuptools.find_packages(".", exclude=["tests*"]),
    install_requires=[
        "requests",
        "urllib3",
        "PrettyTable",
        "python-keycloak-client",
        "PyJWT",
        "jsonschema",
    ],
    data_files=[
        (
            "schema",
            [
                "origo/pipelines/resources/schemas/pipelines.json",
                "origo/pipelines/resources/schemas/pipeline-instances.json",
                "origo/pipelines/resources/schemas/pipeline-inputs.json",
                "origo/pipelines/resources/schemas/schemas.json",
            ],
        )
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
