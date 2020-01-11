import dataclasses
import datetime
import decimal
import typing


@dataclasses.dataclass
class KV:
    da: datetime.date
    a: datetime.date
    tipo: str
    conto_bancoposta: str
    intestato_a: str
    saldo_al: datetime.date
    saldo_contabile: decimal.Decimal
    saldo_disponibile: decimal.Decimal


@dataclasses.dataclass
class Row:
    data_contabile: datetime.date
    data_valuta: datetime.date
    addebiti: typing.Optional[decimal.Decimal]
    accrediti: typing.Optional[decimal.Decimal]
    descrizione_operazioni: str
