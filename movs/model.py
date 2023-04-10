from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import ClassVar


@dataclass(frozen=True)
class KV:
    da: date | None
    a: date | None
    tipo: str
    conto_bancoposta: str
    intestato_a: str
    saldo_al: date | None
    saldo_contabile: Decimal
    saldo_disponibile: Decimal


@dataclass(frozen=True)
class Row:
    zero: ClassVar[Decimal] = Decimal(0)

    data_contabile: date
    data_valuta: date
    addebiti: Decimal | None
    accrediti: Decimal | None
    descrizione_operazioni: str

    @property
    def money(self) -> Decimal:
        if self.addebiti is not None:
            return -self.addebiti
        if self.accrediti is not None:
            return self.accrediti
        return Row.zero

    @property
    def date(self) -> date:
        return self.data_valuta

class Rows(list[Row]):
    def __init__(self, name: str, iterable: Iterable[Row]=()):
        super().__init__(iterable)
        self.name = name
