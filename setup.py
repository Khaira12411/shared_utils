from setuptools import setup, find_packages

setup(
    name="shared_utils",
    version="0.1.0",
    packages=find_packages(include=["pokemon_utils", "pokemon_utils.*"]),
    python_requires=">=3.11",
    description="Shared utilities for multiple bots",
    author="Khy",
    url="https://github.com/Khaira12411/shared_utils",
)