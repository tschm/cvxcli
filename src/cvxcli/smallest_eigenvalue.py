#    Copyright 2023 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Module for computing the smallest eigenvalue of matrices stored in BSON files.

This module provides functionality to read matrices from BSON files and compute
their smallest eigenvalues, which is useful in various convex optimization problems.
"""

import fire  # type: ignore
import numpy as np
from cvx.bson.file import read_bson


def smallest_ev(bson_file) -> dict[str, float]:
    """Compute the smallest eigenvalue of matrices stored in a bson file.

    There are faster methods to compute the smallest eigenvalue, e.g. an inverse power iteration.
    Here, we only use this as an example to work with the bson interface.

    On the command line

    poetry run smallest-eigenvalue cli/data/test.bson
    """
    eigenvalues = {key: np.min(np.linalg.eigh(matrix)[0]) for key, matrix in read_bson(bson_file).items()}

    for key, ev in eigenvalues.items():
        print(key, ev)

    return eigenvalues


def main():  # pragma: no cover
    """Command-line entry point for the smallest eigenvalue calculator.

    Uses the Fire library to expose the smallest_ev function as a command-line tool.
    """
    fire.Fire(smallest_ev)
