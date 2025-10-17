import pytest
import random
from copy import deepcopy

from project.smart_args import smart_args, Evaluated, Isolated


def test_copy_argument():
    """Test basic copy of Isolated arguments"""

    @smart_args
    def check_isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    orig = {"a": 10}
    no_mutable = check_isolation(d=orig)
    assert no_mutable == {"a": 0}
    assert orig == {"a": 10}


def test_only_named_arguments():
    """Test named arguments"""

    @smart_args
    def func(*, x=2):
        return x

    with pytest.raises(TypeError) as excinfo:
        func(10)
    assert str(excinfo.value) == "Error: smart args need named arguments"


def test_missing_argument():
    """Test missing arguments"""

    @smart_args
    def func(*, x):
        return x

    with pytest.raises(TypeError) as excinfo:
        func()
    assert str(excinfo.value) == "Error: argument x is not provided"


def test_evaluated_isolated_together():
    """Test Evaluated and Isolated together"""

    def get_val():
        return 2

    @smart_args
    def func(*, x=Evaluated(get_val), y=Isolated()):
        return x, y

    with pytest.raises(TypeError) as excinfo:
        func()
    assert str(excinfo.value) == "Error: argument y must be Isolated"


def test_evaluated_random():
    """Test defaults with random numbers"""

    def get_random_number():
        return random.randint(0, 100)

    @smart_args
    def check_evaluation(*, x=get_random_number(), y=Evaluated(get_random_number)):
        return (x, y)

    x1, y1 = check_evaluation()
    x2, y2 = check_evaluation()
    x3, y3 = check_evaluation(y=150)
    assert x1 == x2 and x2 == x3
    assert y3 == 150


def test_evaluated_directly():
    """Test that argument can't get Evaluated directly"""

    def get_val():
        return 2

    @smart_args
    def func(*, x=Evaluated(get_val)):
        return x

    with pytest.raises(AssertionError) as excinfo:
        func(x=Evaluated(get_val))
    assert str(excinfo.value) == "Error: argument x gets Evaluated object directly"


def test_isolated_directly():
    """Test that argument can't get Isolated directly"""

    @smart_args
    def func(*, y=Isolated()):
        return y

    with pytest.raises(AssertionError) as excinfo:
        func(y=Isolated())
    assert str(excinfo.value) == "Error: argument y gets Isolated object directly"


def test_combined_argument():
    """Test function with combined arguments"""

    @smart_args
    def func(*, a=Isolated(), b=10):
        return a, b

    result = func(a={"key": 5})
    assert result[0] == {"key": 5}
    assert result[1] == 10


def test_dynamic_evaluated():
    """Test dynamic Evaluated"""
    val = {"key": 0}

    def get_val():
        val["key"] += 1
        return val["key"]

    @smart_args
    def func(*, x=Evaluated(get_val)):
        return x

    val1 = func()
    assert val1 == 1
    val2 = func()
    assert val2 == 2


def test_evaluated_callable():
    """Test Evaluated with not a callable function"""

    with pytest.raises(TypeError) as excinfo:
        Evaluated(5)
    assert str(excinfo.value) == "Must be initialized with a callable function."
