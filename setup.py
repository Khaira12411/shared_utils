from setuptools import setup, find_packages

setup(
    name="pokemon_utils",  # name of your package
    version="0.1.0",  # start at 0.1.0
    packages=find_packages(),  # automatically find packages in the folder
    install_requires=[],  # add dependencies if your code needs any
    python_requires=">=3.11",  # match your bots' Python version
    description="Shared Pokémon utilities for multiple bots",
    author="YourName",
    url="https://github.com/yourusername/pokemon-utils",  # repo URL
)
