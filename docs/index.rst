.. birkhkoff documentation master file, created by
   sphinx-quickstart on Mon Mar 31 19:03:33 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Birkhoff--von Neumann decomposition of doubly stochastic matrices
=================================================================

This package provides Birkhoff's algorithm for computing the Birkhoff--von
Neumann decomposition of a doubly stochastic matrix.

`Source code`_ · `Packaging`_ · `Issues`_

.. _Source code: https://github.com/jfinkels/birkhoff
.. _Packaging: https://pypi.python.org/pypi/birkhoff
.. _Issues: https://github.com/jfinkels/birkhoff/issues

Installation
------------

.. sourcecode:: bash

   pip install birkhoff


Basic usage
-----------

.. sourcecode:: python

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


Mathematical background
-----------------------

A *doubly stochastic matrix* is a matrix in which each row and each column sum
to one. In other words, a matrix :math:`D` is doubly stochastic if

.. math::

   D 1 & = 1 \\
   1^T D & = 1^T

A *permutation matrix* is a matrix in which each entry is either zero or one.
By the `Birkhoff--von Neumann Theorem`_, each doubly stochastic matrix is a
convex combination of permutation matrices.  In other words, for each :math:`n
\times n` doubly stochastic matrix :math:`D`, there is a sequence of real
numbers :math:`\alpha_1, \dotsc, \alpha_N` and permutation matrices :math:`P_1,
\dotsc, P_N` such that

.. math::

   D = \sum_{i = 1}^N \alpha_i P_i

where :math:`\sum_{i = 1}^N \alpha_i = 1` and the number :math:`N` is
guaranteed to be at most :math:`n^2`. Furthermore, the proof of the
Birkhoff--von Neumann Theorem provides an explicit algorithm for computing each
:math:`\alpha_i` and :math:`P_i`. This is the algorithm employed by
the :func:`~birkhoff.birkhoff_von_neumann_decomposition` function.

The theorem and corresponding algorithm also apply to scalar multiples of
doubly stochastic matrices, that is, matrices of the form :math:`c D`, for some
positive real number :math:`c`.

.. _Birkhoff--von Neumann Theorem: https://en.wikipedia.org/wiki/Doubly_stochastic_matrix#Birkhoff_polytope_and_Birkhoff.E2.80.93von_Neumann_theorem

Birkhoff's Algorithm
~~~~~~~~~~~~~~~~~~~~

Describe the algorithm here.

API
---

.. module:: birkhoff

.. autofunction:: birkhoff_von_neumann_decomposition


Changes
-------

0.0.5
.....

Released on December 19, 2017.

- Updated code to work with NetworkX version 2.0 (issue #3).
