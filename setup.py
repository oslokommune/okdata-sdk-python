import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="okdata-sdk",
    version="3.1.1",
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
        "jsonschema",
        # Versions prior to 3.9.1 depends on the vulnerable (and seemingly
        # abandoned) python-jose library.
        "python-keycloak>=3.9.1,<4",
        "requests>=2.25,<3",
        "urllib3>=1.26,<2",
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
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    zip_safe=False,
)
