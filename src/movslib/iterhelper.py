from collections.abc import Iterable
from itertools import pairwise
from typing import cast
from typing import overload


@overload
def zip_with_next[T](
    it: 'Iterable[T]', last: None
) -> 'Iterable[tuple[T, None]]': ...
@overload
def zip_with_next[T](it: 'Iterable[T]', last: T) -> 'Iterable[tuple[T, T]]': ...
def zip_with_next[T](
    it: 'Iterable[T]', last: T | None
) -> 'Iterable[tuple[T, T | None]]':
    return cast(Iterable[tuple[T, T | None]], pairwise((*it, last)))
