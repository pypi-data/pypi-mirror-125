"""Install Gradient Model package."""

import io
import sys
from os import path

from setuptools import setup
# from setuptools import find_packages
from setuptools.command.test import test as TestCommand


root = path.abspath(path.dirname(__file__))


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(path.join(root, filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


long_description = read('README.md')

setup(
    name="gradientmodel",
    version="0.0.2",
    author="John Garrett",
    author_email="garrettj403@gmail.com",
    description="Calculate the surface impedance of a rough metal surface using the Gradient Model (GM)",
    license="MIT",
    url="https://github.com/garrettj403/GradientModel/",
    # keywords=[],
    # packages=find_packages(),
    py_modules=['gradientmodel'],
    install_requires=[
        'numpy',
        'scipy',
        'mpmath',
        ],
    extras_require={
        # 'testing': ['pytest'],
        'examples': ['matplotlib', ], },
    # tests_require=['pytest'],
    # cmdclass={'test': PyTest},
    long_description=long_description,
    long_description_content_type='text/markdown',
    platforms='any',
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7", ],
    project_urls={
        'Changelog': 'https://github.com/garrettj403/GradientModel/blob/master/CHANGES.md',
        'Issue Tracker': 'https://github.com/garrettj403/GradientModel/issues', },
    # scripts=[],
)
