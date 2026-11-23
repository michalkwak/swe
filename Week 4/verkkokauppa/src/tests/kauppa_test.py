import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        viitegeneraattori_mock.uusi.return_value = 42

        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista


class TestKauppaTilisiirtoArguments(unittest.TestCase):
    def setUp(self):
        self.bank_mock = Mock()
        self.reference_mock = Mock()
        self.reference_mock.uusi.return_value = 42

        self.stock_mock = Mock()
        stock = {1: 10, 2: 5, 3: 0}
        products = {
            1: Tuote(1, "milk", 5),
            2: Tuote(2, "bread", 3),
            3: Tuote(3, "butter", 7),
        }
        self.stock_mock.saldo.side_effect = lambda product_id: stock[product_id]
        self.stock_mock.hae_tuote.side_effect = lambda product_id: products[product_id]

        self.shop = Kauppa(self.stock_mock, self.bank_mock, self.reference_mock)
        self.shop.aloita_asiointi()

    def test_payment_with_one_product_calls_tilisiirto_with_correct_arguments(self):
        self.shop.lisaa_koriin(1)
        self.shop.tilimaksu("pekka", "12345")

        self.bank_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_payment_with_two_different_products_calls_tilisiirto_with_correct_arguments(self):
        self.shop.lisaa_koriin(1)
        self.shop.lisaa_koriin(2)
        self.shop.tilimaksu("pekka", "12345")

        self.bank_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 8)

    def test_payment_with_two_of_the_same_product_calls_tilisiirto_with_correct_arguments(self):
        self.shop.lisaa_koriin(1)
        self.shop.lisaa_koriin(1)
        self.shop.tilimaksu("pekka", "12345")

        self.bank_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)

    def test_payment_with_in_stock_and_out_of_stock_product_only_charges_in_stock_one(self):
        self.shop.lisaa_koriin(1)
        self.shop.lisaa_koriin(3)
        self.shop.tilimaksu("pekka", "12345")

        self.bank_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)
