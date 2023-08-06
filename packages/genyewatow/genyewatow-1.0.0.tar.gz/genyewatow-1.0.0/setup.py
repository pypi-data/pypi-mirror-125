import setuptools
from setuptools import setup
import genyewatow


setup(
    name="genyewatow",
    version=genyewatow.__version__,
    author="ombe1229",
    author_email="h3236516@gmail.com",
    description="Awesome owo text genyewatow",
    license="WTFPL License",
    packages=setuptools.find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ombe1229/Genyewatow",
)
