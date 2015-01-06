# birkhoff.py - computes Birkhoff decomposition of a doubly stochastic matrix
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
"""Provides a function for computing the Birkhoff decomposition of a doubly
stochastic matrix.

"""
import itertools

import numpy as np

#: The current version of this package.
__version__ = '0.0.1-dev'


def to_permutation_matrix(dimension, edges):
    """Converts a set of edges into a permutation matrix.

    `dimension` is the size of the permutation matrix.

    Pre-condition: `edges` must be the graph of a permutation.

    Returns a permutation matrix as a square NumPy array.

    """
    P = np.zeros((dimension, dimension))
    # TODO Is there a cleverer way of doing this?
    for (i, j) in edges:
        P[i, j] = 1
    return P


def perfect_matching(B):
    """Returns the set of edges representing a perfect matching in the
    bipartite graph whose biadjacency matrix is `B`.

    `B` must be a NumPy array.

    This function returns a :class:`frozenset` of edges represented as pairs of
    vertices, assuming vertices are numbered from **0** to **m - 1** on the
    left and **0** to **n - 1** on the right, where **m** and **n** are the
    numbers of vertices in the left and right vertex sets of the graph
    represented by `B`, respectively.

    """
    # This is a naive algorithm that simply takes a greedy assignment.
    matching = set()
    matched_vertices = set()
    (m, n) = B.shape
    edges = zip(*B.nonzero())
    for (i, j) in edges:
        # If either i or j have already been matched, just continue. Otherwise,
        # add the edge to the matching and mark its vertices as matched.
        if i not in matched_vertices and j not in matched_vertices:
            matching.add((i, j))
            matched_vertices.add(i)
            matched_vertices.add(j)
    return frozenset(matching)


def to_bipartite_matrix(A):
    """Returns the adjacency matrix of a bipartite graph whose biadjacency
    matrix is `A`.

    `A` must be a NumPy array.

    If `A` has **m** rows and **n** columns, then the returned matrix has **m +
    n** rows and columns.

    """
    m, n = A.shape
    return np.vstack((np.hstack(np.zeros((m, m)), A),
                      np.hstack(A.T, np.zeros((n, n)))))


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


def birkhoff_decomposition(D):
    """Returns the Birkhoff decomposition of the doubly stochastic matrix `D`.

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

    """
    (m, n) = D.shape
    if m != n:
        raise ValueError('Input matrix must be square ({} x {})'.format(m, n))
    indices = list(itertools.product(range(m), range(n)))
    coefficients = []
    permutations = []
    i = 0
    while not np.all(D == 0):
        print('iteration {}'.format(i))
        i += 1
        print('D matrix')
        print(D)
        # Create an undirected graph whose adjacency matrix contains a 1
        # exactly where the matrix D has a nonzero entry.
        W = to_pattern_matrix(D)
        print('pattern matrix')
        print(W)
        X = to_bipartite_matrix(W)
        print('bipartite matrix')
        print(X)
        # Compute a perfect matching for the graph.
        M = perfect_matching(X)
        print('matching:', M)
        # Convert that perfect matching to a permutation matrix.
        P = to_permutation_matrix(n, M)
        print('permutation matrix')
        print(P)
        # Get the smallest entry of D corresponding to the 1 entries in the
        # permutation matrix.
        q = min(D[i, j] for (i, j) in indices if P[i, j] == 1)
        print('coefficient:', q)
        # Store the coefficient and the permutation matrix for later.
        coefficients.append(q)
        permutations.append(P)
        # Subtract P scaled by q. After this subtraction, D has a zero entry
        # where the value q used to live.
        D -= q * P
    return list(zip(coefficients, permutations))
