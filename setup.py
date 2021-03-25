"""pyramid_route_7 installation script.
"""
import os
import re

from setuptools import setup
from setuptools import find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

long_description = description = "micro-templating extensions to Pyramid routing"
with open(os.path.join(HERE, "README.rst")) as f:
    long_description = f.read()

# store version in the init.py
with open(os.path.join(HERE, "src", "pyramid_route_7", "__init__.py")) as v_file:
    VERSION = re.compile(r'.*__VERSION__ = "(.*?)"', re.S).match(v_file.read()).group(1)

requires = [
    "pyramid",
]
tests_require = [
    "pytest",
    "webtest",
]
testing_extras = tests_require + []

setup(
    name="pyramid_route_7",
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_route_7",
    version=VERSION,
    description=description,
    long_description=long_description,
    keywords="web pyramid routing routes",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    extras_require={
        "testing": testing_extras,
    },
    test_suite="tests",
)
