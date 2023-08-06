from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1'
DESCRIPTION = 'Load all your recon data to burp'


# Setting up
setup(
    name="burpLoader",
    version=VERSION,
    author="karthithehacker",
    author_email="<contact@karthithehacker.com>",
    description=DESCRIPTION,
    install_requires=[],
    keywords=['python', 'burp', 'burpLoader'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
