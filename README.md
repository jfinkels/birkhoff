# Birkhoff's algorithm for doubly stochastic matrices #

This package contains a Python 3 implementation of Birkhoff's algorithm for
decomposing a doubly stochastic matrix into a convex combination of permutation
matrices.

For more information, see `the full documentation
<http://birkhoff.readthedocs.org>`_.

This file was last updated on January 7, 2015.

## Copyright license ##

This package is distributed under the terms of the GNU General Public License
version 3. For more information, see the file `LICENSE` in this directory.

## Basic usage ##

    import numpy
    from birkhoff import birkhoff_von_neumann_decomposition

    # Create a doubly stochastic matrix.
    #
    # D = numpy.array(...)

    # The decomposition is given as a list of pairs in which the right element
    # is a permutation matrix and the left element is the scalar coefficient
    # applied to that permutation matrix in the convex combination
    # representation of the doubly stochastic matrix.
    result = birkhoff_von_neumann_decomposition(D)
    for coefficient, permutation_matrix in result:
        print('coefficient:', coefficient)
        print('permutation matrix:', permutation_matrix)

## Installation requirements ##

In order to install the Python libraries required to use this package:

    pip install -r requirements.txt

Testing
-------

    pip install -r requirements-test.txt
    nosetests

Release instructions
--------------------

This is a reminder for the maintainer of this package.

    python setup.py egg_info sdist upload --sign

Contact
-------

Jeffrey Finkelstein <jeffrey.finkelstein@gmail.com>
