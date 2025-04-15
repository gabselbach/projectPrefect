"""Este é o arquivo de configuração base do projeto"""
from setuptools import setup
from setuptools import find_packages

setup(
    name="projectprefect",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)