from setuptools import setup, find_packages

setup(
    name="basil-calculib",
    version="0.1.0.dev",
    packages=find_packages(),

    description="Calculators and analyzers library.",
    install_requires=["basil_common==0.1.0.dev",
                      "redis==2.10.5",
                      "requests==2.9.1"],
)
