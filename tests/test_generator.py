import pytest
from functools import reduce
from typing import Any, Generator, List
from project.generator import generate, pipeline, results


def map_of_square(x):
    """Function generates squared values"""
    return map(lambda v: v**2, x)


def filter_for_even(x):
    """Function generates even values"""
    return filter(lambda v: v % 2 == 0, x)


def enumerate_pair(x):
    """Function enumerates values"""
    return enumerate(x, start=1)


def zip_with_range(x):
    """Function generates pairs of values"""
    return zip(x, range(1, 5))


def reduce_multiply(x):
    """Function multiplys all values"""
    return (y for y in [reduce(lambda a, b: a * b, x, 1)])


def increment_gen(x):
    """Function increments values"""
    return (v + 1 for v in x)


def divisible_filter(x):
    """Function generates values divisible by 5"""
    return filter(lambda v: v % 5 == 0, x)


@pytest.fixture
def val():
    """Provides a list of integers for future tests"""
    return [1, 2, 3, 4]


def test_generate_val(val):
    """Test generate function"""
    res = generate(val[0], val[-1])
    assert list(res) == [1, 2, 3, 4]


@pytest.mark.parametrize(
    "operations, expected",
    [
        # map: squares of numbers
        (map_of_square, [1, 4, 9, 16]),
        # filter: keep even numbers
        (filter_for_even, [2, 4]),
        # enumerate: pair each value with index
        (enumerate_pair, [(1, 1), (2, 2), (3, 3), (4, 4)]),
        # zip: combine elements with a range
        (zip_with_range, [(1, 1), (2, 2), (3, 3), (4, 4)]),
        # reduce: multiply all elements together
        (reduce_multiply, [24]),
        # function: increment each element
        (increment_gen, [2, 3, 4, 5]),
        # empty result
        (divisible_filter, []),
    ],
)
def test_pipeline_operations(val, operations, expected):
    """Tests the pipeline function"""
    res = pipeline(generate(val[0], val[-1]), operations)
    assert list(res) == expected


@pytest.mark.parametrize(
    "collector, expected",
    [(list, [1, 2, 3, 4]), (set, {1, 2, 3, 4}), (tuple, (1, 2, 3, 4)), (sum, 10)],
)
def test_collect_results(val, collector, expected):
    """Tests the results function"""
    stream = generate(val[0], val[-1])
    res = results(stream, collector)
    assert res == expected


def map_times2_filter_gt2(x):
    """Function multiplys each element by 2 and filters values greater than 2"""
    return filter(lambda v: v > 2, map(lambda v: v * 2, x))


def enumerate_identity(x):
    """Function enumerates values"""
    return enumerate(x)


@pytest.mark.parametrize(
    "operations, collector, expected",
    [
        # map and filter combination
        (map_times2_filter_gt2, set, {4, 6, 8}),
        # enumerate results in dictionary
        (enumerate_identity, dict, {0: 1, 1: 2, 2: 3, 3: 4}),
    ],
)
def test_multiple_pipeline_operations(val, operations, collector, expected):
    """Tests the multiple operations"""
    res = pipeline(generate(val[0], val[-1]), operations)
    collected = results(res, collector)
    assert collected == expected


def test_custom_function(val):
    """Test custom function"""

    def double(stream):
        for v in stream:
            yield v * 2

    result = pipeline(generate(val[0], val[-1]), double)
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

    res = pipeline(generate(val[0], val[-1]), count)
    assert number["count"] == 0
    first = next(res)
    assert first == first_elem
    assert number["count"] == 1
