import unittest
from ostoskori import Ostoskori
from tuote import Tuote

class TestOstoskori(unittest.TestCase):
    def setUp(self):
        self.kori = Ostoskori()

    def test_ostoskorin_hinta_ja_tavaroiden_maara_alussa(self):
        self.assertEqual(self.kori.hinta(), 0)
        self.assertEqual(self.kori.tavaroita_korissa(), 0)

    # step 1
    def test_ostoskorin_hinta_ja_tuotteiden_maara_alussa(self):
        self.assertEqual(self.kori.hinta(), 0)
        

    # step 2
    def test_yhden_tuotteen_lisaamisen_jalkeen_korissa_yksi_tavara(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        self.assertEqual(self.kori.tavaroita_korissa(), 1)

    def test_cart_price_the_same_as_product_price(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        self.assertEqual(self.kori.hinta(), 3)
        
    def test_after_adding_two_different_products_cart_has_two_items(self):
        maito = Tuote("Maito", 3)
        leipa = Tuote("Leipä", 4)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(leipa)
        self.assertEqual(self.kori.tavaroita_korissa(), 2)

    def test_after_adding_two_different_products_cart_price_is_sum_of_product_prices(self):
        maito = Tuote("Maito", 3)
        leipa = Tuote("Leipä", 4)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(leipa)
        self.assertEqual(self.kori.hinta(), 7)

    def test_after_adding_two_of_the_same_product_cart_has_two_items(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(maito)
        self.assertEqual(self.kori.tavaroita_korissa(), 2)

    def test_after_adding_two_of_the_same_product_cart_price_is_twice_the_product_price(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(maito)
        self.assertEqual(self.kori.hinta(), 6)

    def test_after_adding_one_product_cart_contains_one_purchase(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        ostokset = self.kori.ostokset()
        self.assertEqual(len(ostokset), 1)

    def test_after_adding_one_product_cart_contains_purchase_with_product_name_and_quantity_one(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        ostos = self.kori.ostokset()[0]
        self.assertEqual(ostos.tuotteen_nimi(), "Maito")
        self.assertEqual(ostos.lukumaara(), 1)

    def test_after_adding_two_different_products_cart_contains_two_purchases(self):
        maito = Tuote("Maito", 3)
        leipa = Tuote("Leipä", 4)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(leipa)
        self.assertEqual(len(self.kori.ostokset()), 2)
