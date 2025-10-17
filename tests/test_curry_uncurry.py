import pytest

from project.curry import curry_explicit, uncurry_explicit


def test_curry_and_uncurry():
    """Test basic curry and uncurry"""
    f2 = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)
    g2 = uncurry_explicit(f2, 3)
    assert f2(123)(456)(562) == "<123,456,562>"
    assert g2(123, 456, 562) == "<123,456,562>"


def test_zero_arity():
    """Test functions with zero arity"""

    def func():
        return 5

    def func2():
        return "Hi"

    curry = curry_explicit(func, 0)
    uncurry = uncurry_explicit(curry, 0)
    assert curry() == 5
    assert uncurry() == 5
    curry2 = curry_explicit(func2, 0)
    uncurry2 = uncurry_explicit(curry2, 0)
    assert curry2() == func2()
    assert uncurry2() == func2()


def test_one_arity():
    """Test function with one arity"""

    def func(x):
        return x + 5

    curry = curry_explicit(func, 1)
    uncurry = uncurry_explicit(curry, 1)
    assert curry(2) == 7
    assert uncurry(2) == 7


def test_curry_negative_arity():
    """Test negative arity curry"""

    def func(x):
        return x

    with pytest.raises(ValueError) as excinfo:
        curry_explicit(func, -1)
    assert str(excinfo.value) == "Arity can't be negative"


def test_uncurry_negative_arity():
    """Test negative arity uncurry"""

    def func(x):
        return x

    curry = curry_explicit(func, 1)
    with pytest.raises(ValueError) as excinfo:
        uncurry_explicit(curry, -1)
    assert str(excinfo.value) == "Arity can't be negative"


def test_curry_uncurry_fixed_arity():
    """Test curry and uncurry with fixed arity"""

    def func(*args):
        return sum(args)

    curry = curry_explicit(func, 4)
    assert curry(1)(2)(3)(4) == 10
    uncurry = uncurry_explicit(curry, 4)
    assert uncurry(1, 2, 3, 4) == 10


def test_curry_each_argument():
    """Test that curried function takes one argument each time"""

    def f(x, y):
        return x / y

    curry = curry_explicit(f, 2)
    res1 = curry(100)
    with pytest.raises(TypeError):
        res1(20, 30)
    res2 = res1(20)
    assert res2 == 5


def test_curry_more_arguments():
    """Test curry with more arguments than expected"""

    def func(x, y):
        return x * y

    curry = curry_explicit(func, 2)
    with pytest.raises(TypeError) as excinfo:
        curry(1, 2, 3)
    assert str(excinfo.value) == "More arguments than expected"


def test_uncurry_less_arguments():
    """Test uncurry with less arguments than expected"""

    def f(x, y, z):
        return x + y - z

    curry = curry_explicit(f, 3)
    uncurry = uncurry_explicit(curry, 3)
    with pytest.raises(TypeError) as excinfo:
        uncurry(1, 2)
    assert str(excinfo.value) == "Error: expected 3 arguments, but got 2 arguments"


def test_uncurry_more_arguments():
    """Test uncurry with more arguments than expected"""

    def f(x, y):
        return x + y

    curry = curry_explicit(f, 2)
    uncurry = uncurry_explicit(curry, 2)
    with pytest.raises(TypeError) as excinfo:
        uncurry(1, 2, 3)
    assert str(excinfo.value) == "Error: expected 2 arguments, but got 3 arguments"


def test_curry_built_in_function():
    """Test curry built-in functions"""
    curry = curry_explicit(print, 2)
    assert curry(1)(2) is None
    curry_len = curry_explicit(len, 1)
    vec = [1, 2, 3, 4]
    assert curry_len(vec) == 4
    curry_pow = curry_explicit(pow, 2)
    assert curry_pow(5)(3) == 125
