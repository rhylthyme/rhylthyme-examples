#!/usr/bin/env python3
"""
Setup script for Rhylthyme Examples
"""

import os

from setuptools import setup


# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Rhylthyme Examples - Example programs and environments for Rhylthyme"


setup(
    name="rhylthyme-examples",
    version="0.1.0-alpha",
    description="Example programs and environments for Rhylthyme real-time scheduling system",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Rhylthyme Team",
    author_email="team@rhylthyme.org",
    url="https://github.com/rhylthyme/rhylthyme-examples",
    # No packages to install - this is just for testing
    packages=[],
    install_requires=[
        # Core dependencies needed to validate examples
        "rhylthyme-cli-runner>=0.1.0-alpha",
        "rhylthyme-spec>=0.1.0-alpha",
    ],
    extras_require={
        "dev": [
            # Testing framework
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "pytest-mock>=3.0.0",
            # Code quality
            "black>=21.0.0",
            "flake8>=3.8.0",
            "isort>=5.0.0",
        ],
    },
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Distributed Computing",
    ],
    keywords="real-time, scheduling, logistics, examples, validation",
    project_urls={
        "Bug Reports": "https://github.com/rhylthyme/rhylthyme-examples/issues",
        "Source": "https://github.com/rhylthyme/rhylthyme-examples",
        "Documentation": "https://github.com/rhylthyme/rhylthyme-examples#readme",
    },
)
