"""
Matrix operations test module
"""

import math
import pytest
from project.matrix import transpose, add, multiply
from typing import List


def test_empty_transpose():
    """Test transpose of empty matrix"""
    m = []
    assert transpose(m) == []


def test_transpose():
    """Test transpose of matrix"""
    m = [[1, 2], [3, 4]]
    assert transpose(m) == [[1, 3], [2, 4]]


def test_wrong_transpose():
    """Test transpose of wrong matrix"""
    m = [[1, 2], [3, 4]]
    assert transpose(m) != [[1, 2], [3, 4]]


def test_add_empty_matrix():
    """Test addition of two matrices with one empty matrix"""
    m1 = []
    m2 = [[1, 2], [3, 4]]
    assert add(m1, m2) == [[1, 2], [3, 4]]


def test_add_matrices():
    """Test addition of two matrices"""
    m1 = [[11, 15], [32, 64]]
    m2 = [[15, 62], [72, 28]]
    assert add(m1, m2) == [[26, 77], [104, 92]]


def test_wrong_add_matrices():
    """Test of wrong addition of two matrices"""
    m1 = [[1, 2], [8, 9]]
    m2 = [[5, 6], [3, 4]]
    assert add(m1, m2) != [[7, 8], [9, 10]]


def test_different_size_matrices_add():
    """Test addition of matrices with different sizes"""
    m1 = [[1, 2, 4], [8, 9, 5]]
    m2 = [[5, 6], [3, 4]]
    with pytest.raises(ValueError) as excinfo:
        add(m1, m2)
    assert str(excinfo.value) == "The matrices have different sizes."


def test_empty_multiplication():
    """Test addition of two matrices with one empty matrix"""
    m1 = []
    m2 = [[1, 2], [2, 1]]
    assert multiply(m1, m2) == []


def test_one_value_multiplication():
    """Test addition of two matrices with one row and column"""
    m1 = [[1, 2]]
    m2 = [[3], [2]]
    assert multiply(m1, m2) == [[7]]


def test_simple_multiplication():
    """Test addition of two matrices"""
    m1 = [[1, 2], [3, 4]]
    m2 = [[1, 2], [3, 4]]
    assert multiply(m1, m2) == [[7, 10], [15, 22]]


def test_wrong_multiplication():
    """Test wrong addition of two matrices"""
    m1 = [[11, 15], [32, 64]]
    m2 = [[15, 62], [72, 28]]
    assert multiply(m1, m2) != [[26, 77], [104, 92]]


def test_multiplication():
    """Test addition of two matrices"""
    m1 = [[1, 2, 3], [4, 5, 6]]
    m2 = [[1, 1], [2, 2], [3, 3]]
    assert multiply(m1, m2) == [[14, 14], [32, 32]]


def test_raise_multiplication():
    """Test addition of two matrices where the number of columns of the first matrix is different to the number of rows of the second matrix"""
    m1 = [[5, 6], [3, 4], [5, 6]]
    m2 = [[1, 2, 4], [8, 9, 5], [2, 4, 5]]
    with pytest.raises(ValueError) as excinfo:
        multiply(m1, m2)
    assert (
        str(excinfo.value)
        == "The number of columns of the first matrix is different to the number of rows of the second matrix."
    )
