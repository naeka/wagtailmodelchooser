#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
from setuptools import setup


name = 'wagtailmodelchooser'
package = 'wagtailmodelchooser'
description = 'Wagtail chooser panel generator for generic Django models'
url = 'https://github.com/Naeka/wagtailmodelchooser'
author = 'Naeka'
author_email = 'leo@naeka.fr'
license = 'BSD'


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("^__version__ = ['\"]([^'\"]+)['\"]",
                     init_py, re.MULTILINE).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


version = get_version(package)


if sys.argv[-1] == 'publish':
    if os.system("pip freeze | grep wheel"):
        print("wheel not installed.\nUse `pip install wheel`.\nExiting.")
        sys.exit()
    os.system("python setup.py sdist upload")
    os.system("python setup.py bdist_wheel upload")
    print("You probably want to also tag the version now:")
    print("  git tag -a {0} -m 'version {0}'".format(version))
    print("  git push --tags")
    sys.exit()


install_requires = [
    'Django>=1.8.1,<1.11',
    'wagtail>=1.5',
]

# Testing dependencies
testing_extras = [
    # Required for running the tests
    'pytest-django>=2.9,<2.10',
    'pytest>=2.9,<2.10',
    'pytest-cov>=2.2',
    'flake8>=2.4.0',

    # For PyPI installs
    'wheel==0.24.0',
]

# Documentation dependencies
documentation_extras = [
    'mkdocs==0.11.1',
]


setup(
    name=name,
    version=version,
    url=url,
    license=license,
    description=description,
    author=author,
    author_email=author_email,
    packages=get_packages(package),
    package_data=get_package_data(package),
    install_requires=install_requires,
    extras_require={
        'testing': testing_extras,
        'docs': documentation_extras
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
    ]
)
