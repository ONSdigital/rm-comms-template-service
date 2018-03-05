from setuptools import setup, find_packages

NAME = "RM Comms Template"
VERSION = "1.0.0"

REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    description="Comms Template API",
    author_email="rm@ons.gov.uk",
    url="",
    keywords=["Comms Template API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    long_description="RM Comms Template microservice."
)
