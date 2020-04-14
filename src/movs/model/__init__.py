import dataclasses
import datetime
import decimal
import typing


@dataclasses.dataclass(frozen=True)
class KV:
    da: typing.Optional[datetime.date]
    a: typing.Optional[datetime.date]
    tipo: str
    conto_bancoposta: str
    intestato_a: str
    saldo_al: typing.Optional[datetime.date]
    saldo_contabile: decimal.Decimal
    saldo_disponibile: decimal.Decimal


@dataclasses.dataclass(frozen=True)
class Row:
    data_contabile: datetime.date
    data_valuta: datetime.date
    addebiti: typing.Optional[decimal.Decimal]
    accrediti: typing.Optional[decimal.Decimal]
    descrizione_operazioni: str
