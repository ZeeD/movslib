from itertools import chain
from typing import Iterable
from typing import Optional
from typing import Tuple
from typing import TypeVar

T = TypeVar('T')


def zip_with_next(it: Iterable[T],
                  last: Optional[T]) -> Iterable[Tuple[T, Optional[T]]]:
    c = chain(it, (last, ))
    next(c)
    return zip(it, c)
