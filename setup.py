import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="origo-sdk",
    version="0.3.0",
    author="Oslo Origo",
    author_email="dataplattform@oslo.kommune.no",
    description="SDK for origo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/origo-sdk-python",
    package_data={"origo": ["py.typed"]},
    packages=setuptools.find_namespace_packages(
        include="origo.sdk.*", exclude=["tests*"]
    ),
    install_requires=[
        "requests",
        "urllib3",
        "PrettyTable",
        "python-keycloak",
        "PyJWT",
        "jsonschema",
    ],
    data_files=[
        (
            "schema",
            [
                "origo/sdk/pipelines/resources/schemas/pipelines.json",
                "origo/sdk/pipelines/resources/schemas/pipeline-instances.json",
                "origo/sdk/pipelines/resources/schemas/pipeline-inputs.json",
                "origo/sdk/pipelines/resources/schemas/schemas.json",
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
    python_requires=">=3.6",
    zip_safe=False,
)
