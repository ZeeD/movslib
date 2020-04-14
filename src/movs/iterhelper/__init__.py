import itertools
import typing


T = typing.TypeVar('T')


def zip_with_next(it: typing.Iterable[T], last: typing.Optional[T]
                  ) -> typing.Iterable[typing.Tuple[T, typing.Optional[T]]]:
    c = itertools.chain(it, (last, ))
    next(c)
    return zip(it, c)
