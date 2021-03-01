import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="okdata-sdk",
    version="0.6.3",
    author="Oslo Origo",
    author_email="dataplattform@oslo.kommune.no",
    description="SDK for origo dataplatform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/okdata-sdk-python",
    package_data={"okdata": ["py.typed"]},
    packages=setuptools.find_namespace_packages(
        include="okdata.sdk.*", exclude=["tests*"]
    ),
    namespace_packages=["okdata"],
    install_requires=[
        "requests",
        "urllib3",
        "PrettyTable",
        "python-keycloak",
        "PyJWT>=2.0.0",
        "jsonschema",
    ],
    data_files=[
        (
            "schema",
            [
                "okdata/sdk/pipelines/resources/schemas/pipelines.json",
                "okdata/sdk/pipelines/resources/schemas/pipeline-instances.json",
                "okdata/sdk/pipelines/resources/schemas/pipeline-inputs.json",
                "okdata/sdk/pipelines/resources/schemas/schemas.json",
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
