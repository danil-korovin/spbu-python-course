from typing import Any, Callable
from copy import deepcopy
from functools import wraps
import inspect


class Isolated:
    """Class indicates that argument must be copied"""

    pass


class Evaluated:
    """
    Wraps dynamicly default value

    Args:
        func (Callable[[], Any]): Returns value to use by default.
    """

    def __init__(self, func: Callable[[], Any]) -> None:
        if not callable(func):
            raise TypeError("Must be initialized with a callable function.")
        self.func = func


def smart_args(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator which provides named Evaluated and Isolated

    Args:
        func (Callable[..., Any]): Function to decorate.

    Returns:
        Callable[..., Any]: Wrapped function with smart argument.

    Raises:
        TypeError: smart args need named arguments
        TypeError: argument {name} must be Isolated
        TypeError: argument {name} is not provided
    Assert:
        AssertionError: argument {name} gets Evaluated object directly
        AssertionError: argument {name} gets Isolated object directly

    """
    s = inspect.signature(func)

    @wraps(func)
    def wrapped(*args: Any, **kwargs: Any) -> Any:
        if args:
            raise TypeError("Error: smart args need named arguments")

        kwargs_new = {}
        for name, par in s.parameters.items():

            if name in kwargs:
                value = kwargs[name]
                if isinstance(par.default, Isolated):
                    value = deepcopy(value)
                assert not isinstance(
                    value, Evaluated
                ), f"Error: argument {name} gets Evaluated object directly"
                assert not isinstance(
                    value, Isolated
                ), f"Error: argument {name} gets Isolated object directly"

            else:
                default = par.default
                if isinstance(default, Evaluated):
                    value = default.func()
                elif isinstance(default, Isolated):
                    raise TypeError(f"Error: argument {name} must be Isolated")
                elif default is par.empty:
                    raise TypeError(f"Error: argument {name} is not provided")
                else:
                    value = default

            kwargs_new[name] = value

        return func(**kwargs_new)

    return wrapped
