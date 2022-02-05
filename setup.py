# -*- encoding: utf-8 -*-

from setuptools import find_packages, setup

dev_requires = [
    "black",
    "flake8",
    "flake8-black",
    "mypy",
    "pytest",
]

setup(
    # Name of the package:
    name="bain-wizard-interpreter",
    # Version of the package:
    version="0.0.3",
    # Find the package automatically (include everything):
    packages=find_packages(exclude=("tests",)),
    package_data={"wizard": ["py.typed"]},
    # Author information:
    author="Holt59",
    author_email="capelle.mikael@gmail",
    # Description of the package:
    description="A BAIN Wizard Interpreter based on wizparse.",
    long_description=open("README.md").read(),
    # URL for sources:
    url="https://github.com/Holt59/bain-wizard-interpreter",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    # License:
    license="MIT",
    # Requirements:
    install_requires=[
        "chardet",
        "antlr4-python3-runtime==4.9.2",
    ],
    extras_require={"dev": dev_requires},
)
