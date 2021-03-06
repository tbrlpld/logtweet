# -*- coding: utf-8 -*-

"""Setup script."""

from setuptools import setup  # type: ignore

with open("README.md", "r") as f:
    long_description = f.read()

requires = [
    "bs4",
    "requests",
    "tweepy",
    "validators",
]

develop_requires = [
    "wheel",
    # "twine" to upload to pypi in secure way.
    # See: https://packaging.python.org/tutorials/packaging-projects/
    "twine",
    "pytest",
    "pytest-cov",
    "wemake-python-styleguide",
    "mypy",
]

setup(
    name="logtweet",
    version="0.1.5dev",
    author="Tibor Leupold",
    author_email="tibor@lpld.io",
    description="Create a tweet based on a #100DaysOfCode log message",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tbrlpld/logtweet",
    python_requires=">=3.6",
    install_requires=requires,
    extras_require={
        "develop": develop_requires,
    },
    packages=["logtweet"],
    entry_points={
        "console_scripts": [
            "logtweet = logtweet.app:main",
        ],
    },
    include_package_data=True,  # To copy the files listen in MANIFEST.in
)
