# test_birkhoff.py - unit tests for Birkhoff decomposition
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
"""Unit tests for the :mod:`birkhoff` module.

"""
from __future__ import division

import numpy as np

from birkhoff import birkhoff_decomposition


def test_birkhoff_decomposition():
    D = (1 / 6) * np.array([[1, 4, 0, 1],
                            [2, 1, 3, 0],
                            [2, 1, 1, 2],
                            [1, 0, 2, 3]])
    P1 = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]])
    P2 = np.identity(4)
    P3 = np.array([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
    P4 = np.array([[0, 1, 0, 0], [0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1]])
    expected_coefficients = [1 / 6, 1 / 6, 1 / 3, 1 / 3]
    expected_permutations = [P1, P2, P3, P4]
    print(birkhoff_decomposition(D))
    actual_coefficients, actual_permutations = zip(*birkhoff_decomposition(D))
    assert sorted(actual_coefficients) == sorted(expected_coefficients)
    assert sorted(actual_permutations) == sorted(expected_permutations)
