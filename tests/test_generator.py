import pytest
from functools import reduce
from typing import Any, Generator, List
from project.generator import generate, conveyor, results


@pytest.fixture
def val():
    """Provides a list of integers for future tests"""
    return [1, 2, 3, 4]


def test_generate_val(val):
    """Test generate function"""
    res = generate(val)
    assert list(res) == [1, 2, 3, 4]


@pytest.mark.parametrize(
    "operations, expected",
    [
        # map: squares of numbers
        (lambda x: map(lambda v: v**2, x), [1, 4, 9, 16]),
        # filter: keep even numbers
        (lambda x: filter(lambda v: v % 2 == 0, x), [2, 4]),
        # enumerate: pair each value with index
        (lambda x: enumerate(x, start=1), [(1, 1), (2, 2), (3, 3), (4, 4)]),
        # zip: combine elements with a range
        (lambda x: zip(x, range(1, 5)), [(1, 1), (2, 2), (3, 3), (4, 4)]),
        # reduce: multiply all elements together
        (lambda x: (y for y in [reduce(lambda a, b: a * b, x, 1)]), [24]),
        # function: increment each element
        (lambda x: (v + 1 for v in x), [2, 3, 4, 5]),
        # empty result
        (lambda x: filter(lambda v: v % 5 == 0, x), []),
    ],
)
def test_conveyor_operations(val, operations, expected):
    """Tests the conveyor function"""
    res = conveyor(val, operations)
    assert list(res) == expected


@pytest.mark.parametrize(
    "collector, expected",
    [(list, [1, 2, 3, 4]), (set, {1, 2, 3, 4}), (tuple, (1, 2, 3, 4)), (sum, 10)],
)
def test_collect_results(val, collector, expected):
    """Tests the results function"""
    stream = generate(val)
    res = results(stream, collector)
    assert res == expected


@pytest.mark.parametrize(
    "operations, collector, expected",
    [
        # map and filter combination
        (lambda x: filter(lambda v: v > 2, map(lambda v: v * 2, x)), set, {4, 6, 8}),
        # enumerate results in dictionary
        (lambda x: enumerate(x), dict, {0: 1, 1: 2, 2: 3, 3: 4}),
    ],
)
def test_multiple_conveyor_operations(val, operations, collector, expected):
    """Tests the multiple operations"""
    res = conveyor(val, operations)
    collected = results(res, collector)
    assert collected == expected


def test_custom_function(val):
    """Test custom function"""

    def double(stream):
        for v in stream:
            yield v * 2

    result = conveyor(val, double)
    assert list(result) == [2, 4, 6, 8]


@pytest.mark.parametrize(
    "operation, first_elem",
    [
        # map:
        (lambda x: map(lambda v: v * 5, x), 5),
    ],
)
def test_lazy_eval(val, operation, first_elem):
    """Test lazy conveyer evaluation"""
    number = {"count": 0}

    def count(stream):
        for elem in operation(stream):
            number["count"] += 1
            yield elem

    res = conveyor(val, count)
    assert number["count"] == 0
    first = next(res)
    assert first == first_elem
    assert number["count"] == 1
