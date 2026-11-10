import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="okdata-sdk",
    version="4.1.0",
    author="Oslo kommune",
    author_email="dataspeilet@oslo.kommune.no",
    description="SDK for data services provided by Oslo kommune",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/okdata-sdk-python",
    package_data={"okdata": ["py.typed"]},
    packages=setuptools.find_namespace_packages(
        include="okdata.sdk.*", exclude=["tests*"]
    ),
    namespace_packages=["okdata"],
    install_requires=[
        # Versions prior to 3.9.1 depends on the vulnerable (and seemingly
        # abandoned) python-jose library.
        "python-keycloak>=3.9.1,<4",
        "requests>=2.25,<3",
        "urllib3>=1.26,<3",
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.15",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    zip_safe=False,
)
