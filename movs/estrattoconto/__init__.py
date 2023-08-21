from datetime import date
from datetime import datetime
from decimal import Decimal
from itertools import count
from math import isnan
from math import nan
from os.path import dirname
from typing import Any
from typing import Literal
from typing import NotRequired
from typing import overload
from typing import TypedDict

from pandas import DataFrame
from tabula.io import read_pdf_with_template

from ..model import KV
from ..model import Row
from ..model import Rows
from ..model import ZERO
from pypdf import PdfReader

TEMPLATE_2 = f'{dirname(__file__)}/template_2.json'
TEMPLATE_3 = f'{dirname(__file__)}/template_3.json'


@overload
def conv_date(dt: str) -> date: ...


@overload
def conv_date(dt: float) -> None: ...


def conv_date(dt: str | float) -> date | None:
    if isinstance(dt, float):
        assert isnan(dt), f'{dt=}'
        return None
    return datetime.strptime(dt, '%d/%m/%y').date()


@overload
def conv_decimal(dec: str) -> Decimal: ...


@overload
def conv_decimal(dec: float) -> None: ...


def conv_decimal(dec: str | float) -> Decimal | None:
    if isinstance(dec, float):
        assert isnan(dec), f'{dec=}'
        return None
    return Decimal(dec.replace('.', '').replace(',', '.'))


def read_kv(tables: list[DataFrame]) -> KV:
    month = tables[0].at[0, 0]
    assert isinstance(month, str), f'{type(month)=}, {month=}'
    da = a = saldo_al = conv_date(month)

    conto_bancoposta = f'{tables[1].at[0,0]:012d}'
    assert isinstance(conto_bancoposta,
                      str), f'{type(conto_bancoposta)=}, {conto_bancoposta=}'

    intestato_a = tables[2].at[0, 0]
    assert isinstance(
        intestato_a, str), f'{type(intestato_a)=}, {intestato_a=}'

    last = tables[-1]
    _, lastrow = list(last.iterrows())[-1]
    _, _, _, accrediti, descr = lastrow.to_list()
    assert isinstance(accrediti, str), f'{type(accrediti)=}, {accrediti=}'
    assert isinstance(descr, str), f'{type(descr)=}, {descr=}'
    assert descr == 'SALDO FINALE'
    saldo_contabile = saldo_disponibile = conv_decimal(accrediti)

    return KV(da,
              a,
              'Tutte',
              conto_bancoposta,
              intestato_a,
              saldo_al,
              ZERO if saldo_contabile is None else saldo_contabile,
              ZERO if saldo_disponibile is None else saldo_disponibile)


# copyed from Row
class TRow(TypedDict):
    data_contabile: NotRequired[date]
    data_valuta: NotRequired[date]
    addebiti: NotRequired[Decimal | None]
    accrediti: NotRequired[Decimal | None]
    descrizione_operazioni: NotRequired[str]


def isnan_(obj: float | str) -> bool:
    return False if isinstance(obj, str) else isnan(obj)


def read_csv(tables: list[DataFrame]) -> list[Row]:
    ret: list[Row] = []

    for table in tables[4:]:
        t_row: TRow = {}
        for _, row in table.iterrows():
            data, valuta, *_,  addebiti, accrediti, descr = row.to_list()
            if all(map(isnan_, [data, valuta, addebiti, accrediti])):
                if not t_row:
                    raise Exception('missing continuation')
                t_row['descrizione_operazioni'] += f' {descr}'
            else:
                if t_row:
                    ret.append(Row(**t_row))
                t_row = {}

                t_row['data_contabile'] = conv_date(data)
                t_row['data_valuta'] = conv_date(valuta)
                t_row['addebiti'] = conv_decimal(addebiti)
                t_row['accrediti'] = conv_decimal(accrediti)
                t_row['descrizione_operazioni'] = descr
        else:
            if t_row:
                ret.append(Row(**t_row))
            t_row = {}

    # drop 'SALDO INIZIALE' and 'SALDO FINALE'
    return ret[1:-1]


@overload
def read_estrattoconto(fn: str) -> tuple[KV, list[Row]]: ...


@overload
def read_estrattoconto(fn: str, name: str) -> tuple[KV, Rows]: ...


def read_estrattoconto(fn: str, name: str | None = None) -> tuple[KV, list[Row] | Rows]:
    template = {
        2: TEMPLATE_2,
        3: TEMPLATE_3,
        10: TEMPLATE_2,  # dicembre
    }[len(PdfReader(fn).pages)]

    tables = read_pdf_with_template(fn,
                                    template,
                                    pandas_options={'header': None})
    assert isinstance(tables, list)
    kv = read_kv(tables)
    csv = read_csv(tables)
    return kv, (list(csv) if name is None else Rows(name, csv))
