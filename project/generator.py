from typing import Any, Generator, Iterable, Callable, Iterator
from functools import reduce


def generate(val: Iterable[Any]) -> Generator[Any, None, None]:
    """
    The function generate converts any iterable object into lazy generator which yields elements one by one.

    Args:
         val: (Iterable[Any]): Any object that supports iteration with any type of elements.

    Yield:
        Generator[Any, None, None]: Generator yields elements of any type from the input iterable.
        YeildType: Any - Generator yields elements of any type.

    Mypy:
        SendType: None - Not used.
        ReturnType: None - Not used.
    """

    for elem in val:
        yield elem


def conveyor(
    val: Iterable[Any],
    *operations: Callable[[Iterator[Any]], Generator[Any, None, None]]
) -> Generator[Any, None, None]:
    """
    The function conveyor creates a lazy data processing conveyor by applying operations to the data stream.

    Args:
        val: Iterable[Any]: The iterable data values of any type.
        *operations: Callable[[Iterator[Any]], Generator[Any, None, None]]: Function that takes Iterator[Any] argument and returns a generator which produces elements of any type.

    Returns:
        Generator[Any, None, None]: Generator that produces transformed data stream.

    Mypy:
        SendType: None - Not used.
        ReturnType: None - Not used.
    """

    stream = generate(val)
    for elem in operations:
        stream = elem(stream)

    return stream


def results(
    stream: Generator[Any, None, None],
    collector: Callable[..., Any] = list,
    *args: Any,
    **kwargs: Any
) -> Any:
    """
    The function collects a lazy data stream into a concrete collection.

    Args:
        stream (Generator[Any, None, None]): Lazy data stream generator where we collect from results.
        collector: Callable[..., Any]: Callable collects different arguments and transform it to concrete form (list by default).
        *args: Additional positional args.
        **kwargs: Additional keyword args.

    Returns:
        The collected result.

    Mypy:
        SendType: None - Not used.
        ReturnType: None - Not used.
    """

    return collector(stream, *args, **kwargs)
