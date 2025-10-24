"""
Setup configuration for cogpy - OpenCog HyperGraphQL implementation
"""
from setuptools import setup, find_packages

setup(
    name="cogpy",
    version="0.1.0",
    description="OpenCog-inspired HyperGraph implementation with GraphQL support",
    author="cogpy",
    packages=find_packages(),
    install_requires=[
        "graphene>=3.0",
        "flask>=2.3.2",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
