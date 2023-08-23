from datetime import date
from datetime import datetime
from decimal import Decimal
from locale import LC_ALL
from locale import setlocale
from math import isnan
from typing import overload

from tabula.io import read_pdf

from ..model import KV
from ..model import Row
from ..model import Rows


def conv_date(dt: str) -> date:
    return datetime.strptime(dt, '%d/%m/%Y').date()


def conv_kv_date(dt: str) -> date:
    orig = setlocale(LC_ALL)
    setlocale(LC_ALL, 'it_IT.utf8')
    try:
        return datetime.strptime(dt, '%d %B %Y').date()
    finally:
        setlocale(LC_ALL, orig)


@overload
def conv_decimal(dec: str) -> Decimal: ...


@overload
def conv_decimal(dec: float) -> None: ...


def conv_decimal(dec: str | float) -> Decimal | None:
    if isinstance(dec, float):
        assert isnan(dec), f'{dec=}'
        return None
    return Decimal(dec.replace('.', '').replace(',', '.').replace('€', ''))


def read_kv(fn: str) -> KV:
    tables = read_pdf(fn,
                      pandas_options={'header': None},
                      pages=1,
                      area=[
                          [0, 400, 100, 600],
                          [140, 120, 170, 210],
                          [170, 0, 200, 600],
                      ])
    assert isinstance(tables, list)
    data, numero_intestato, saldi = tables
    return KV(None,
              None,
              '',
              numero_intestato.at[0, 0],
              numero_intestato.at[1, 0],
              conv_kv_date(' '.join(data.at[0, 0].split()[:3])),
              conv_decimal(saldi.at[0, 3]),
              conv_decimal(saldi.at[0, 5]))


def read_csv(fn: str) -> list[Row]:
    tables = read_pdf(fn,
                      pages='all',
                      lattice=True)
    assert isinstance(tables, list)
    tables = [table for table in tables if len(table.columns) == 5]
    tables[0].drop(index=0, inplace=True)

    ret: list[Row] = []
    for table in tables:
        for dc, dv, do, ad, ac in table.itertuples(index=False):
            ret.append(Row(conv_date(dc),
                           conv_date(dv),
                           conv_decimal(ad),
                           conv_decimal(ac),
                           do.replace('\r', ' ')))
    return ret


@overload
def read_postepay(fn: str) -> tuple[KV, list[Row]]: ...


@overload
def read_postepay(fn: str, name: str) -> tuple[KV, Rows]: ...


def read_postepay(fn: str, name: str | None = None) -> tuple[KV, list[Row] | Rows]:
    kv = read_kv(fn)
    csv = read_csv(fn)

    return kv, (list(csv) if name is None else Rows(name, csv))
