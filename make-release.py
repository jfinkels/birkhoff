#!/usr/bin/env python3
#
# make-release.py - facilitates releasing and publishing versions of a package
#
# Copyright (c) 2011 by Armin Ronacher.
# Copyright 2014 Jeffrey Finkelstein.
#
# Some rights reserved.
#
# Redistribution and use in source and binary forms of the software as well as
# documentation, with or without modification, are permitted provided that the
# following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * The names of the contributors may not be used to endorse or promote
#   products derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE AND DOCUMENTATION IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE AND
# DOCUMENTATION, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""Updates versions for, tags, and publishes a release of a Python package.

This script requires Python 3.

To use this script::

    $ ./make-release.py

This script assumes your versions conform to `semantic versioning`_. By
default, it increments the patch number in the version number (for example,
2.7.1 to 2.7.2). In order to increment a major or minor version number instead
(for example, 2.7.1 to 3.0.0 or 2.7.1 to 2.8.0, respectively), specify either
``major`` or ``minor`` as the sole argument to the script::

    $ ./make-release.py major
    $ ./make-release.py minor

.. _semantic versioning: http://semver.org/

"""
import os.path
import re
from subprocess import Popen
from subprocess import PIPE
import sys

#: The name of the top-level Python package containing the code for this
#: project, that is, the name of the directory containing the __init__.py file.
#PACKAGE = 'birkhoff'
MODULE = 'birkhoff.py'

#: The variable containing the version string in the __init__.py file.
INIT_VERSION_STRING = '__version__'

#: The keyword containing the version string in the setup.py file.
SETUP_VERSION_STRING = 'version'


def bump_version(version, which=None):
    """Returns the result of incrementing `version`.

    If `which` is not specified, the "patch" part of the version number will be
    incremented.  If `which` is specified, it must be ``'major'``, ``'minor'``,
    or ``'patch'``. If it is one of these three strings, the corresponding part
    of the version number will be incremented instead of the patch number.

    Returns a string representing the next version number.

    Example::

        >>> bump_version('2.7.1')
        '2.7.2'
        >>> bump_version('2.7.1', 'minor')
        '2.8.0'
        >>> bump_version('2.7.1', 'major')
        '3.0.0'

    """
    try:
        parts = [int(n) for n in version.split('.')]
    except ValueError:
        fail('Current version is not numeric')
    if len(parts) != 3:
        fail('Current version is not semantic versioning')
    # Determine where to increment the version number
    PARTS = {'major': 0, 'minor': 1, 'patch': 2}
    index = PARTS[which] if which in PARTS else 2
    # Increment the version number at that index and set the subsequent parts
    # to 0.
    before, middle, after = parts[:index], parts[index], parts[index + 1:]
    middle += 1
    return '.'.join(str(n) for n in before + [middle] + after)


def set_version(filename, version_number, pattern):
    changed = []

    def inject_version(match):
        before, old, after = match.groups()
        changed.append(True)
        return before + version_number + after
    with open(filename) as f:
        contents = re.sub(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern,
                          inject_version, f.read())
    if not changed:
        fail('Could not find {} in {}'.format(pattern, filename))
    with open(filename, 'w') as f:
        f.write(contents)


def get_version(filename, pattern):
    """Gets the current version from the specified file.

    This function assumes the file includes a string of the form::

        <pattern> = <version>

    """
    with open(filename) as f:
        match = re.search(r"^(\s*%s\s*=\s*')(.+?)(')(?sm)" % pattern, f.read())
    if match:
        before, version, after = match.groups()
        return version
    fail('Could not find {} in {}'.format(pattern, filename))


def build_and_upload():
    """Uses Python's setup.py commands to build the package and upload it to
    PyPI.

    """
    Popen([sys.executable, 'setup.py', 'egg_info', 'sdist', 'upload',
           '--sign']).wait()
    #Popen([sys.executable, 'setup.py', 'publish']).wait()


def fail(message=None, exit_status=None):
    """Prints the specified message and exits the program with the specified
    exit status.

    """
    print('Error:', message, file=sys.stderr)
    sys.exit(exit_status or 1)


def git_tags():
    """Returns a list of the git tags."""
    process = Popen(['git', 'tag'], stdout=PIPE)
    return set(process.communicate()[0].splitlines())


def git_is_clean():
    """Returns ``True`` if and only if there are no uncommitted changes."""
    return Popen(['git', 'diff', '--quiet']).wait() == 0


def git_commit(message):
    """Commits all changed files with the specified message."""
    Popen(['git', 'commit', '-am', message]).wait()


def git_tag(tag):
    """Tags the current version."""
    print('Tagging "{}"'.format(tag))
    msg = '"Released version {}"'.format(tag)
    Popen(['git', 'tag', '-s', '-m', msg, tag]).wait()


def main():
    # Determine the current version and compute the next development version.
    #init_filename = os.path.join(PACKAGE, '__init__.py')
    version = get_version(MODULE, INIT_VERSION_STRING)
    if version.endswith('-dev'):
        version = version[:-4]

    # Check if the current version has already been tagged, or if it it not
    # ready to be published.
    print('Releasing {}'.format(version))
    if version in git_tags():
        fail('Version {} is already tagged'.format(version))
    if not git_is_clean():
        fail('You have uncommitted changes in git')

    # Set the version string in __init__ and setup.py to be current version.
    set_version(init_filename, version, INIT_VERSION_STRING)
    set_version('setup.py', version, SETUP_VERSION_STRING)

    # Commit and tag the current version in git.
    git_commit('Bump version number to {}'.format(version))
    git_tag(version)

    # Use Python's setup.py to build and upload the package to PyPI.
    build_and_upload()

    # Set the version string in __init__ and setup.py to be the next version.
    which_part = sys.argv[1] if len(sys.argv) > 1 else None
    dev_version = bump_version(version, which_part) + '-dev'
    set_version(MODULE, dev_version, INIT_VERSION_STRING)
    set_version('setup.py', dev_version, SETUP_VERSION_STRING)
    #add_new_changelog_section(version, dev_version)
    git_commit('Set development version number to {}'.format(dev_version))


if __name__ == '__main__':
    main()
