#!/usr/bin/env python

import movs


def main() ->None:
    fn = 'resources/BPOL_Lista_Movimenti.txt'
    kv, csv = movs.read_txt(fn)
    print(f'kv: {kv}')
    for row in csv:
        print(f'row: {row}')

    fn += "DELME"
    print('-'*80)

    movs.write_txt(fn, kv, csv)
    kv, csv = movs.read_txt(fn)
    print(f'kv: {kv}')
    for row in csv:
        print(f'row: {row}')


if __name__ == '__main__':
    main()
