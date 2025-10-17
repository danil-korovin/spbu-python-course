from typing import Any, Callable


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Convert a function with several arguments into a curried function.

    Args:
        function: The given function.
        arity: Number of arguments of curried function.

    Returns:
        A curried function.

    Raises:
        ValueError: Arity can't be negative
        TypeError: More arguments than expected
    """
    if arity < 0:
        raise ValueError("Arity can't be negative")

    if arity == 0:

        def zero() -> Any:
            return function()

        return zero

    def curry(*args: Any) -> Any:

        if len(args) == arity:
            return function(*args)

        if len(args) > arity:
            raise TypeError("More arguments than expected")

        return lambda elem: curry(*args, elem)

    return curry


def uncurry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Convert a curried function back into a function.

    Args:
        function: The curried function.
        arity: Number of arguments, which expected by the curried function.

    Returns:
        Function which accepts all arguments at ones.

    Raises:
        ValueError: Arity can't be negative".
        TypeError: Error: expected {arity} arguments, but got {len(args)} arguments.
    """
    if arity < 0:
        raise ValueError("Arity can't be negative")

    if arity == 0:

        def zero() -> Any:
            return function()

        return zero

    def uncurry(*args: Any) -> Any:

        if len(args) != arity:
            raise TypeError(
                f"Error: expected {arity} arguments, but got {len(args)} arguments"
            )

        func = function
        for elem in args:
            func = func(elem)
        return func

    return uncurry
