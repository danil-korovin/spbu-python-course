"""
Vector operations test module
"""

import math
import pytest
from project.vector import length, dot_product, angle
from typing import List


def test_zero_length():
    """Test length of zero vector"""
    v = []
    assert length(v) == 0


def test_length():
    """Test length of vector"""
    v = [3, 4]
    assert length(v) == 5


def test_wrong_length():
    """Test length of vector"""
    v = [3, 4]
    assert length(v) != 6


def test_dot_product():
    """Test dot product of two vectors"""
    v1 = [1, 2, 3]
    v2 = [1, 2, 3]
    assert dot_product(v1, v2) == 14.0


def test_raise_dot_product():
    """Test dot product of two vectors with different lengths"""
    v1 = [1, 2, 3]
    v2 = [1, 2]
    with pytest.raises(ValueError) as excinfo:
        dot_product(v1, v2)
    assert str(excinfo.value) == "Vectors have different lengths."


def test_angle_90():
    """Test angle between two orthogonal vectors"""
    v1 = [1, 0]
    v2 = [0, 1]
    assert angle(v1, v2) == math.pi / 2


def test_angle_0():
    """Test angle between two parallel vectors"""
    v1 = [1, 0]
    v2 = [2, 0]
    assert angle(v1, v2) == 0


def test_raise1_angle():
    """Test angle between two vectors with different lengths"""
    v1 = [1, 2, 3]
    v2 = [1, 2]
    with pytest.raises(ValueError) as excinfo:
        angle(v1, v2)
    assert str(excinfo.value) == "Vectors have different lengths."


def test_raise2_angle():
    """Test angle between two vectors with zero lenght"""
    v1 = [0, 0]
    v2 = [0, 0]
    with pytest.raises(ValueError) as excinfo:
        angle(v1, v2)
    assert str(excinfo.value) == "Angle is undefined for zero length vector."
