import logging

import movs


def main() ->None:
    fn = 'resources/BPOL_Lista_Movimenti.txt'
    kv, csv = movs.read_txt(fn)
    logging.warning('kv: %s', kv)
    for row in csv:
        logging.warning('row: %s', row)


if __name__ == '__main__':
    main()
