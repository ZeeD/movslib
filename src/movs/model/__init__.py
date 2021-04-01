from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional


@dataclass(frozen=True)
class KV:
    da: Optional[date]
    a: Optional[date]
    tipo: str
    conto_bancoposta: str
    intestato_a: str
    saldo_al: Optional[date]
    saldo_contabile: Decimal
    saldo_disponibile: Decimal


@dataclass(frozen=True)
class Row:
    data_contabile: date
    data_valuta: date
    addebiti: Optional[Decimal]
    accrediti: Optional[Decimal]
    descrizione_operazioni: str
