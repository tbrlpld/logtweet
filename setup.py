# -*- coding: utf-8 -*-

"""Setup script."""

from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

requires = [
    "bs4",
    "requests",
    "tweepy",
]

develop_requires = [
    "wheel",
    # "twine" to upload to pypi in secure way.
    # See: https://packaging.python.org/tutorials/packaging-projects/
    "twine",
]

setup(
    name="logtweet",
    version="0.1.2",
    author="Tibor Leupold",
    author_email="tibor@lpld.io",
    description="Create a tweet based on a #100DaysOfCode log message",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tbrlpld/100daysofweb-with-python-course/tree/master/work/078-twitter-bot",
    python_requires=">=3.6",
    install_requires=requires,
    extras_require={
        "develop": develop_requires,
    },
    packages=["logtweet"],
    entry_points={
        "console_scripts": [
            "logtweet = logtweet:main",
        ],
    },
    include_package_data=True,  # To copy the files listen in MANIFEST.in
)
