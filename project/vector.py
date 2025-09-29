"""
Vector operations module
"""

import math
from typing import List


def length(vec: list[float]) -> float:
    """
    Caculates the length of a vector.

    Args:
        vec: Vector.

    Returns:
        Length of given vector.
    """
    if len(vec) == 0:
        return 0.0

    return sum([i**2 for i in vec]) ** 0.5


def dot_product(vec1: list[float], vec2: list[float]) -> float:
    """
    Calculates dot product of two vectors.

    Args:
        vec1: First vector.
        vec2: Second vector.

    Returns:
        Dot product of two vectors: vec1 and vec2.

    Raises:
        ValueError: If vectors have different lengths.
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors have different lengths.")

    return sum(vec1[i] * vec2[i] for i in range(len(vec1)))


def angle(vec1: list[float], vec2: list[float]) -> float:
    """
    Calculates angle between two vectors.

    Args:
        vec1: First vector.
        vec2: Second vector.

    Returns:
        Angle in radians.

    Raises:
        ValueError: If vectors have different lengths or one of them is zero.
    """
    if len(vec1) != len(vec2):
        raise ValueError("Vectors have different lengths.")

    len_vec1 = length(vec1)
    len_vec2 = length(vec2)
    dot_prod = dot_product(vec1, vec2)

    if len_vec1 == 0 or len_vec2 == 0:
        raise ValueError("Angle is undefined for zero length vector.")

    angle = dot_prod / (len_vec1 * len_vec2)
    return math.acos(angle)
