#!/usr/bin/env python

from sys import argv

from . import read_scansioni


def check_scansioni(fn: str) -> None:
    print(f'{fn=}')

    kv, rows = read_scansioni(fn)

    iniziale_money = kv.saldo_contabile
    finale_money = kv.saldo_disponibile

    print(f'{iniziale_money=}')
    print(f'{finale_money=}')
    actual = sum((row.money for row in rows), iniziale_money)
    print(f'      {actual=}')
    assert finale_money == actual, f'{finale_money-actual=}'


def main() -> None:
    for fn in argv[1:]:
        check_scansioni(fn)


if __name__ == '__main__':
    main()
