import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medgpt",
    version="0.3.0",
    author="w-is-h",
    author_email="w.kraljevic@gmail.com",
    description="Temporal modeling of patients and diseases",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/w-is-h/medgpt",
    packages=['medgpt', 'medgpt.datasets', 'medgpt.metrics', 'medgpt.utils', 'medgpt.models'],
    install_requires=[
        'datasets~=1.14.0',
        'ray==1.3.0',
        'wandb~=0.10',
        'x-transformers~=0.20',
        'ecco==0.0.14',
        'transformers~=4.11.3',
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
