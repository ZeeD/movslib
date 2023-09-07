from sys import argv

from tabula.io import read_pdf


def main() -> None:
    for fn in argv[1:]:
        print(f'{fn=}')
        tables = read_pdf(fn, pages=1, pandas_options={'header': None})
        print(f'{len(tables)=}')
        for table in tables:
            print('-----------------------')
            print(table)


if __name__ == '__main__':
    main()
