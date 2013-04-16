from distutils.core import setup
from setuptools import find_packages

setup(
    name='pyutillib',
    version='0.1.0',
    author='Edwin van Opstal',
    author_email='evo.se-technology.com',
    url='http://github.com/EdwinvO/pyutillib',
    license='LICENSE.txt',
    description='Small collection of python functions',
    long_description=open('README.rst').read(),
    install_requires=[
    ],
    packages=find_packages(),
)
