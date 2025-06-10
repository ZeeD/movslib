from typing import TYPE_CHECKING
from typing import overload

if TYPE_CHECKING:
    from movslib.model import KV
    from movslib.model import Row
    from movslib.model import Rows


@overload
def read_buoni_csv(fn: str) -> 'tuple[KV, list[Row]]': ...


@overload
def read_buoni_csv(fn: str, name: str) -> 'tuple[KV, Rows]': ...


def read_buoni_csv(
    fn: str, name: str | None = None
) -> 'tuple[KV, list[Row] | Rows]':
    raise NotImplementedError
