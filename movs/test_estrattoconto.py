from datetime import date
from decimal import Decimal
from os.path import dirname
from unittest import main
from unittest import TestCase

from .estrattoconto import read_estrattoconto
from .model import Row

PATH = f'{dirname(__file__)}/../test_estrattoconto.pdf'


class TestEstrattoconto(TestCase):
    def test_base(self) -> None:
        kv, rows = read_estrattoconto(PATH)

        # kv
        self.assertEqual(date(2022, 8, 31), kv.da)
        self.assertEqual(date(2022, 8, 31), kv.a)
        self.assertEqual('Tutte', kv.tipo)
        self.assertEqual('001030700957', kv.conto_bancoposta)
        self.assertEqual('CHREIM ELENA DE TULLIO VITO', kv.intestato_a)
        self.assertEqual(date(2022, 8, 31), kv.saldo_al)
        self.assertEqual(Decimal('350.85'), kv.saldo_contabile)
        self.assertEqual(Decimal('350.85'), kv.saldo_disponibile)

        # rows
        self.assertEqual([
            Row(date(2022, 07, 31), None, None, Decimal('468.80'), 'SALDO INIZIALE'),
Row(date(2022, 08, 01), date(2022, 08, 01), None, Decimal('1.500,00'), 'BONIFICO TRN BAPPIT22 5034004217772210480160001753IT'),
Row(None, None, None, None, 'DA CHREIM ELENA PER Viaggio America'),
Row(date(2022, 08, 01), date(2022, 08, 01), Decimal('1.500,00'), None, 'RICARICA POSTEPAY DA WEB/APP Ricarica Postepay'),
Row(date(2022, 08, 01), date(2022, 08, 01), Decimal('1.00'), None, 'COMMISSIONE RICARICA POSTEPAY Ricarica Postepay'),
Row(date(2022, 08, 02), date(2022, 07, 31), Decimal('2.00'), None, 'CANONE CONTO CLICK ADDEBITO RELATIVO AL PERIODO DI'),
Row(None, None, None, None, 'LUGLIO 2022'),
Row(date(2022, 08, 02), date(2022, 07, 30), Decimal('16.82'), None, 'PAGAMENTO POS 30/07/2022 11.39 COOP LOMBARDIA S.C.'),
Row(None, None, None, None, 'SESTO SAN GIO ITA OPERAZIONE 652381 CARTA 92051516'),
Row(date(2022, 08, 02), date(2022, 07, 29), Decimal('22.00'), None, 'PAGAMENTO POS 29/07/2022 21.08 HAMBU VIMERCATE'),
Row(None, None, None, None, 'VIMERCATE ITA OPERAZIONE 657526 CARTA 92051516'),
Row(date(2022, 08, 02), date(2022, 07, 29), Decimal('36.50'), None, 'PAGAMENTO POS 29/07/2022 20.35 BESTIA BEER E STREET'),
Row(None, None, None, None, 'F VIMERCATE ITA OPERAZIONE 659080 CARTA 92051516'),
Row(date(2022, 08, 03), date(2022, 07, 31), Decimal('29.00'), None, 'PAGAMENTO POS 31/07/2022 22.11 FANCYTOAST MILANO ITA'),
Row(None, None, None, None, 'OPERAZIONE 659917 CARTA 92051516'),
Row(date(2022, 08, 04), date(2022, 08, 04), Decimal('201.00'), None, 'ADDEBITO DIRETTO SDD A2A SPA'),
Row(None, None, None, None, 'CID.IT17ENE0000011957540153 040822'),
Row(None, None, None, None, 'MAN.00000000000000000000007020761594001'),
Row(date(2022, 08, 05), date(2022, 08, 03), Decimal('69.50'), None, 'PAGAMENTO POS 03/08/2022 20.49 YAMAMOTO SRL MILANO'),
Row(None, None, None, None, 'ITA OPERAZIONE 654684 CARTA 92051516'),
Row(date(2022, 08, 07), date(2022, 08, 07), None, Decimal('400.00'), 'POSTAGIRO TRN BPPIITRR'),
Row(None, None, None, None, 'EA22080727947325PO0400004000IT DA DE TULLIO VITO'),
Row(None, None, None, None, 'GELAO MARIA PER Agosto 2022'),
Row(date(2022, 08, 07), date(2022, 08, 07), Decimal('250.00'), None, 'POSTAGIRO TRN EA22080727951725PO0160020400IT BENEF'),
Row(None, None, None, None, 'Elena Cavagnis PER Regalo da Vito e Elena per i neo'),
Row(None, None, None, None, 'sposi. Vi auguriamo ogni be'),
Row(date(2022, 08, 08), date(2022, 07, 31), Decimal('1.00'), None, 'CANONE MENSILE CARTA DI DEBITO MESE DI RIFERIMENTO'),
Row(None, None, None, None, '2022/07'),
Row(date(2022, 08, 08), date(2022, 07, 31), Decimal('1.00'), None, 'CANONE MENSILE CARTA DI DEBITO MESE DI RIFERIMENTO'),
Row(None, None, None, None, '2022/07'),
Row(date(2022, 08, 09), date(2022, 08, 07), Decimal('7.50'), None, 'PAGAMENTO POS 07/08/2022 09.43 LLOA BE NATURAL'),
Row(None, None, None, None, 'MILANO ITA OPERAZIONE 650894 CARTA 92051516'),
Row(date(2022, 08, 09), date(2022, 08, 07), Decimal('39.89'), None, 'PAGAMENTO POS 07/08/2022 12.37 COOP LOMBARDIA S.C.'),
Row(None, None, None, None, 'SESTO SAN GIO ITA OPERAZIONE 652851 CARTA 92051516'),
Row(date(2022, 08, 09), date(2022, 08, 09), None, Decimal('400.00'), 'POSTAGIRO TRN BPPIITRR'),
Row(None, None, None, None, 'EA22080929158352PO0400004000IT DA DE TULLIO VITO'),
Row(None, None, None, None, 'GELAO MARIA PER Agosto 2022'),
Row(date(2022, 08, 09), date(2022, 08, 09), None, Decimal('400.00'), 'BONIFICO TRN BAPPIT22 5034000457292220480160001753IT'),
Row(None, None, None, None, 'DA CHREIM ELENA PER Agosto ele'),
Row(date(2022, 08, 09), date(2022, 08, 09), Decimal('626.92'), None, 'BONIFICO TRN EA22080931258833480160020400IT BENEF'),
Row(None, None, None, None, 'BANCA DI CREDITO COOPERATIVO PER Gestione ordinaria'),
Row(None, None, None, None, "2022/2023 unita': 07, 31 1"),
Row(date(2022, 08, 10), date(2022, 08, 07), Decimal('18.10'), None, 'PAGAMENTO POS 07/08/2022 11.44 1 H CLEAN DI ROZZA'),
Row(None, None, None, None, 'GIU SESTO SAN GIO ITA OPERAZIONE 656532 CARTA'),
Row(None, None, None, None, '92051516'),
Row(date(2022, 08, 10), date(2022, 08, 10), None, Decimal('400.00'), 'BONIFICO TRN BAPPIT22 5034000470672221480160001753IT'),
Row(None, None, None, None, 'DA CHREIM ELENA PER Settembre Ele'),
Row(date(2022, 08, 11), date(2022, 08, 10), Decimal('6.45'), None, 'PAGAMENTO POS 10/08/2022 10.51 3584 MARKET MILANO'),
Row(None, None, None, None, 'MILANO ITA OPERAZIONE 669267 CARTA 92051516'),
Row(date(2022, 08, 17), date(2022, 08, 13), Decimal('7.00'), None, 'PAGAMENTO POS 13/08/2022 09.22 SumUp *Sun Strac Map'),
Row(None, None, None, None, 'Milano ITA OPERAZIONE 669406 CARTA 92051516'),
Row(date(2022, 08, 17), date(2022, 08, 13), Decimal('30.10'), None, 'PAGAMENTO POS 13/08/2022 17.31 COOP LOMBARDIA S.C.'),
Row(None, None, None, None, 'SESTO SAN GIO ITA OPERAZIONE 661180 CARTA 92051516'),
Row(date(2022, 08, 18), date(2022, 08, 15), Decimal('3.90'), None, 'PAGAMENTO POS 15/08/2022 13.21 ROSSOPOMODORO MONZA'),
Row(None, None, None, None, 'ITA OPERAZIONE 665159 CARTA 92051516'),
Row(date(2022, 08, 20), date(2022, 08, 18), Decimal('11.00'), None, 'PAGAMENTO POS 18/08/2022 13.22 CASAVIETNAM DI'),
Row(None, None, None, None, 'NGUYEN. MILANO ITA OPERAZIONE 668501 CARTA 35438808'),
Row(date(2022, 08, 22), date(2022, 08, 22), Decimal('30.22'), None, 'ADDEBITO DIRETTO SDD Wind Tre S.p.'),
Row(None, None, None, None, 'CID.IT960020000013378520152 210822'),
Row(None, None, None, None, 'MAN.O66791531390614'),
Row(date(2022, 08, 22), date(2022, 08, 21), Decimal('3.87'), None, 'PAGAMENTO POS 21/08/2022 11.50 3584 MARKET MILANO'),
Row(None, None, None, None, 'MILANO ITA OPERAZIONE 669376 CARTA 92051516'),
Row(date(2022, 08, 23), date(2022, 08, 20), Decimal('26.47'), None, 'PAGAMENTO POS 20/08/2022 18.57 COOP LOMBARDIA S.C.'),
Row(None, None, None, None, 'SESTO SAN GIO ITA OPERAZIONE 663495 CARTA 92051516'),
Row(date(2022, 08, 26), date(2022, 08, 23), Decimal('100.12'), None, 'PAGAMENTO POS 23/08/2022 19.16'),
Row(None, None, None, None, 'FOREXCHANGE-STAZ.C.GAL MILANO ITA OPERAZIONE 663939'),
Row(None, None, None, None, 'CARTA 92051516'),
Row(date(2022, 08, 26), date(2022, 08, 23), Decimal('101.63'), None, 'PAGAMENTO POS 23/08/2022 19.10'),
Row(None, None, None, None, 'FOREXCHANGE-STAZ.C.GAL MILANO ITA OPERAZIONE 667748'),
Row(None, None, None, None, 'CARTA 92051516'),
Row(date(2022, 08, 27), date(2022, 08, 25), Decimal('2.00'), None, 'PAGAMENTO POS 25/08/2022 12.44 BESTIA BEER E STREET'),
Row(None, None, None, None, 'F VIMERCATE ITA OPERAZIONE 661849 CARTA 92051516'),
Row(date(2022, 08, 30), date(2022, 08, 28), Decimal('8.46'), None, 'PAGAMENTO POS 28/08/2022 11.42 COOP LOMBARDIA S.C.'),
Row(None, None, None, None, 'SESTO SAN GIO ITA OPERAZIONE 669857 CARTA 92051516'),
Row(date(2022, 08, 30), date(2022, 08, 26), Decimal('64.50'), None, 'PAGAMENTO POS 26/08/2022 21.02 MU DELIVERY SRL'),
Row(None, None, None, None, 'MILANO ITA OPERAZIONE 663773 CARTA 92051516'),
Row(date(2022, 08, 31), None, None, Decimal('350.85'), 'SALDO FINALE'),

        ], rows)


if __name__ == '__main__':
    main()
