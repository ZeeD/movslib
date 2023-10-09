#!/usr/bin/env python

from datetime import date
from decimal import Decimal
from sys import argv

from . import read_scansioni


def check_scansioni(fn: str) -> tuple[Decimal, Decimal]:
    print(f'{fn=}')

    kv, rows = read_scansioni(fn)

    data_contabile: date | None = None
    for i, row in enumerate(reversed(rows)):
        assert kv.da, f'{kv.da=}'
        assert kv.da <= row.data_contabile, \
            f'{i=}, {kv.da=}, {row.data_contabile=}'
        assert kv.a, f'{kv.a=}'
        assert row.data_contabile <= kv.a, \
            f'{i=}, {row.data_contabile=}, {kv.a=}'
        assert row.data_valuta <= kv.a, \
            f'{i=}, {row.data_valuta=}, {kv.a=}'

        if data_contabile is not None:
            assert data_contabile <= row.data_contabile, \
                f'{i=}, {data_contabile=}, {row.data_contabile=}'
        data_contabile = row.data_contabile

    iniziale_money = kv.saldo_contabile
    finale_money = kv.saldo_disponibile

    print(f'{iniziale_money=}')
    print(f'{finale_money=}')
    actual = sum((row.money for row in rows), iniziale_money)
    print(f'      {actual=}')
    assert finale_money == actual, f'{finale_money-actual=}'
    return iniziale_money, finale_money


def main() -> None:
    previous_finale: Decimal | None = None
    for fn in argv[1:]:
        iniziale, finale = check_scansioni(fn)
        if previous_finale is not None:
            assert previous_finale == iniziale, f'{previous_finale=}, {iniziale=}'
        previous_finale = finale


if __name__ == '__main__':
    main()
