from typing import Any, Generator, Iterable, Callable, Iterator
from functools import reduce


def generate(start: int, end: int) -> Generator[Any, None, None]:
    """
    The function 'generate' creates a lazy sequence of numbers from start to end inclusive.

    Args:
        start: int: First integer value of the sequence.
        end: int: Last integer value of the sequence (inclusive).

    Yield:
        int: Next integer value in the range from start to end.

    Mypy:
        SendType: None - Not used.
        ReturnType: None - Not used.
    """

    for val in range(start, end + 1):
        yield val


def pipeline(
    val: Iterable[Any], *operations: Callable[[Iterator[Any]], Iterator[Any]]
) -> Iterator[Any]:
    """
    The function pipeline creates a lazy data processing pipeline by applying operations to the data stream.

    Args:
        val: Iterable[Any]: The iterable data values of any type.
        *operations: Callable[[Iterator[Any]], Iterator[Any]]: Function that takes Iterator[Any] argument and returns a iterator which produces elements of any type.

    Returns:
        Iterator[Any]: Generator that produces transformed data stream.

    Mypy:
        SendType: None - Not used.
        ReturnType: None - Not used.
    """

    stream = iter(val)
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
