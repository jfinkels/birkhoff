# birkhoff.py - decompose a doubly stochastic matrix into permutation matrices
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
# A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Birkhoff.  If not, see <http://www.gnu.org/licenses/>.
"""Provides a function for computing the Birkhoff--von Neumann decomposition of
a doubly stochastic matrix into a convex combination of permutation matrices.

"""
# Imports from built-in libraries.
from __future__ import division
import itertools

# Imports from third-party libraries.
from networkx import from_numpy_matrix
import numpy as np

# Imports from this package.
#
# TODO This matching algorithm should really be imported from
# NetworkX. Unfortunately, the algorithm does not yet appear in NetworkX (see
# <https://github.com/networkx/networkx/pull/1322>). Once the algorithm is
# added to NetworkX, we should change this line to
#
#     from networkx.algorithms.bipartite import hopcroft_karp_matching
#
# and remove the module ``matching.py`` entirely.
from matching import hopcroft_karp_matching

#: The current version of this package.
__version__ = '0.0.2'

#: Any number smaller than this will be rounded down to 0 when computing the
#: difference between NumPy arrays of floats.
TOLERANCE = np.finfo(np.float).eps * 10.


def to_permutation_matrix(dimension, matches):
    """Converts a permutation into a permutation matrix.

    `dimension` is the size of the permutation matrix.

    `matches` is a dictionary whose keys are vertices and whose values are
    partners. For each vertex ``u`` and ``v``, entry (``u``, ``v``) in the
    returned matrix will be a ``1`` if and only if ``matches[u] == v``.

    Pre-condition: `matches` must be a permutation on the first `dimension`
    natural numbers.

    Returns a permutation matrix as a square NumPy array.

    """
    P = np.zeros((dimension, dimension))
    # TODO Is there a cleverer way of doing this?
    for (u, v) in matches.items():
        P[u, v] = 1
    return P


def zeros(m, n):
    """Convenience function for ``numpy.zeros((m, n))``."""
    return np.zeros((m, n))


def hstack(left, right):
    """Convenience function for ``numpy.hstack((left, right))``."""
    return np.hstack((left, right))


def vstack(top, bottom):
    """Convenience function for ``numpy.vstack((top, bottom))``."""
    return np.vstack((top, bottom))


def four_blocks(topleft, topright, bottomleft, bottomright):
    """Convenience function that creates a block matrix with the specified
    blocks.

    Each argument must be a NumPy matrix. The two top matrices must have the
    same number of rows, as must the two bottom matrices. The two left matrices
    must have the same number of columns, as must the two right matrices.

    """
    return vstack(hstack(topleft, topright),
                  hstack(bottomleft, bottomright))


def to_bipartite_matrix(A):
    """Returns the adjacency matrix of a bipartite graph whose biadjacency
    matrix is `A`.

    `A` must be a NumPy array.

    If `A` has **m** rows and **n** columns, then the returned matrix has **m +
    n** rows and columns.

    """
    m, n = A.shape
    return four_blocks(zeros(m, m), A, A.T, zeros(n, n))


def to_pattern_matrix(D):
    """Returns the Boolean matrix in the same shape as `D` with ones exactly
    where there are nonzero entries in `D`.

    `D` must be a NumPy array.

    """
    result = np.zeros_like(D)
    # TODO Is there a cleverer way of doing this? Something that sets all the
    # entries at once?
    nonzero_entries = zip(*D.nonzero())
    for (i, j) in nonzero_entries:
        result[i, j] = 1
    return result


def birkhoff_von_neumann_decomposition(D):
    """Returns the Birkhoff--von Neumann decomposition of the doubly stochastic
    matrix `D`.

    The input `D` must be a square NumPy array representing a doubly stochastic
    matrix (that is, a matrix whose entries are nonnegative reals and whose row
    sums and column sums are all 1). Each doubly stochastic matrix is a convex
    combination of at most ``n ** 2`` permutation matrices, where ``n`` is the
    dimension of the input array.

    The returned value is a list of pairs whose length is at most ``n **
    2``. In each pair, the first element is a real number in the interval **(0,
    1]** and the second element is a NumPy array representing a permutation
    matrix. This represents the doubly stochastic matrix as a convex
    combination of the permutation matrices.

    The returned list of pairs is given in the order computed by the algorithm
    (so in particular they are not sorted in any way).

    """
    m, n = D.shape
    if m != n:
        raise ValueError('Input matrix must be square ({} x {})'.format(m, n))
    indices = list(itertools.product(range(m), range(n)))
    # These two lists will store the result as we build it up each iteration.
    coefficients = []
    permutations = []
    # Create a copy of D so that we don't modify it directly.
    S = D.copy()
    while not np.all(S == 0):
        # Create an undirected graph whose adjacency matrix contains a 1
        # exactly where the matrix S has a nonzero entry.
        W = to_pattern_matrix(S)
        # Construct the bipartite graph whose left and right vertices both
        # represent the vertex set of the pattern graph (whose adjacency matrix
        # is ``W``).
        X = to_bipartite_matrix(W)
        # Convert the matrix of a bipartite graph into a NetworkX graph object.
        G = from_numpy_matrix(X)
        # Compute a perfect matching for this graph. The dictionary `M` has one
        # entry for each matched vertex (in both the left and the right vertex
        # sets), and the corresponding value is its partner.
        M = hopcroft_karp_matching(G)
        # However, since we have both a left vertex set and a right vertex set,
        # each representing the original vertex set of the pattern graph
        # (``W``), we need to convert any vertex greater than ``n`` to its
        # original vertex number. To do this,
        #
        #   - ignore any keys greater than ``n``, since they are already
        #     covered by earlier key/value pairs,
        #   - ensure that all values are less than ``n``.
        #
        M = {u: v % n for u, v in M.items() if u < n}
        # Convert that perfect matching to a permutation matrix.
        P = to_permutation_matrix(n, M)
        # Get the smallest entry of S corresponding to the 1 entries in the
        # permutation matrix.
        q = min(S[i, j] for (i, j) in indices if P[i, j] == 1)
        # Store the coefficient and the permutation matrix for later.
        coefficients.append(q)
        permutations.append(P)
        # Subtract P scaled by q. After this subtraction, S has a zero entry
        # where the value q used to live.
        S -= q * P
        # PRECISION ISSUE: There seems to be a problem with floating point
        # precision here, so we need to round down to 0 any entry that is very
        # small.
        S[np.abs(S) < TOLERANCE] = 0.0
    return list(zip(coefficients, permutations))
