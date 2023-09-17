#!/usr/bin/env python

from decimal import Decimal
from sys import argv

from . import read_scansioni


def check_scansioni(fn: str) -> tuple[Decimal, Decimal]:
    print(f'{fn=}')

    kv, rows = read_scansioni(fn)

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
