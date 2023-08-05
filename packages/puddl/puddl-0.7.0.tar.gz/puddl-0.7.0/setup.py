#!/usr/bin/env python
from setuptools import setup, find_packages, find_namespace_packages

setup(
    packages=find_packages() + find_namespace_packages(include=["puddl.*"]),
)
