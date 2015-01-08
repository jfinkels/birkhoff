# setup.py - installation script for this package
#
# Copyright 2015 Jeffrey Finkelstein.
#
# This file is part of Birkhoff.
#
# Birkhoff is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Birkhoff is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Birkhoff.  If not, see <http://www.gnu.org/licenses/>.
"""Birkhoff--von Neumann decomposition for doubly stochastic matrices.

* `Documentation <http://birkhoff.readthedocs.org>`_
* `Packaging <http://pypi.python.org/pypi/birkhoff>`_
* `Source code <http://github.com/jfinkels/birkhoff>`_
* `Issues <http://github.com/jfinkels/birkhoff/issues>`_

"""
from setuptools import setup

#: Installation requirements.
requirements = ['numpy', 'networkx']


setup(
    author='Jeffrey Finkelstein',
    author_email='jeffrey.finkelstein@gmail.com',
    #classifiers=[],
    description=('Birkhoff--von Neumann decomposition for doubly stochastic'
                 ' matrices'),
    download_url='https://github.com/jfinkels/birkhoff',
    install_requires=requirements,
    include_package_data=True,
    #keywords=[],
    license='GNU GPLv3+',
    long_description=__doc__,
    name='birkhoff',
    platforms='any',
    py_modules=['birkhoff'],
    test_suite='nose.collector',
    tests_require=['nose'],
    url='https://github.com/jfinkels/birkhoff',
    version='0.0.2',
    zip_safe=False
)
