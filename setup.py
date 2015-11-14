"""pyramid_route_7 installation script.
"""
import os

from setuptools import setup
from setuptools import find_packages

try:
    here = os.path.abspath(os.path.dirname(__file__))
    README = open(os.path.join(here, "README.md")).read()
    README = README.split("\n\n", 1)[0] + "\n"
except:
    README = ''

requires = [
    "pyramid",
]

setup(
    name="pyramid_route_7",
    version="0.0.2",
    description="extensions to pyramid routing",
    long_description=README,
    classifiers=[
        "Intended Audience :: Developers",
        "Framework :: Pyramid",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="web pyramid",
    py_modules=['pyramid_route_7'],
    author="Jonathan Vanasco",
    author_email="jonathan@findmeon.com",
    url="https://github.com/jvanasco/pyramid_route_7",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    tests_require = requires,
    install_requires = requires,
    test_suite='tests',
)
