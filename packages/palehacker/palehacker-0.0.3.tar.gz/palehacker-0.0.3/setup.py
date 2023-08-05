from setuptools import setup, find_packages
import codecs
import os

ThisD = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(ThisD, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Simple Package'
LONG_DESCRIPTION = 'A package that can get proxies '

setup(
    name="palehacker",
    version=VERSION,
    author="PaleHacker",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/Pale-Hacker/PaleHacker-PyPi",
    packages=find_packages(),
    install_requires=['requests'],
    keywords=['python', 'proxies', 'api', 'requests'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ]
)
