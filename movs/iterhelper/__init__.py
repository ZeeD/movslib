import itertools
import typing


T = typing.TypeVar('T')


def zip_with_next(it: typing.Iterable[T],
                  last: T
                  ) -> typing.Iterable[typing.Tuple[T, T]]:
    c = itertools.chain(it, (last, ))
    next(c)
    return zip(it, c)
