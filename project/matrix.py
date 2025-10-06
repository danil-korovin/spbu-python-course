"""
Matrix operations module
"""

from typing import List


def transpose(m: List[List[float]]) -> List[List[float]]:
    """
    Transpose a matrix.

    Args:
        m: Matrix.

    Returns:
        Transposed matrix.
    """
    if not m:
        return []

    n = len(m)
    k = len(m[0])
    return [[m[i][j] for i in range(n)] for j in range(k)]


def add(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """
    Sum of two matrices.

    Args:
        m1: First matrix.
        m2: Second matrix.

    Returns:
        A new matrix that is the sum of two matrices m1 and m2.

    Raises:
        Error: The matrices have different sizes
    """
    if not m1 and not m2:
        return []
    elif not m1:
        return m2
    elif not m2:
        return m1

    row1 = len(m1)
    col1 = len(m1[0])
    row2 = len(m2)
    col2 = len(m2[0])

    if row1 != row2 or col1 != col2:
        raise ValueError("The matrices have different sizes.")

    res = []
    for i in range(row1):
        row = []
        for j in range(col1):
            row.append(m1[i][j] + m2[i][j])
        res.append(row)
    return res


def multiply(m1: List[List[float]], m2: List[List[float]]) -> List[List[float]]:
    """
    Matrices multiplication.

    Args:
        m1: First matrix.
        m2: Second matrix.

    Returns:
        A new matrix that is the multiplication of two matrices m1 and m2.

    Raises:
        Error: The number of columns of the first matrix is different to the number of rows of the second matrix
    """
    if not m1 or not m2:
        return []

    row1 = len(m1)
    col1 = len(m1[0])
    row2 = len(m2)
    col2 = len(m2[0])

    if col1 != row2:
        raise ValueError(
            "The number of columns of the first matrix is different to the number of rows of the second matrix."
        )

    res = []
    for i in range(row1):
        row = []
        for j in range(col2):
            val = 0.0
            for k in range(len(m2)):
                val += m1[i][k] * m2[k][j]
            row.append(val)
        res.append(row)
    return res
