from tuote import Tuote

class Ostoskori:
    def __init__(self):
        self._tavaroita = 0

    def tavaroita_korissa(self):
        return self._tavaroita

    def hinta(self):
        return 0

    def lisaa_tuote(self, lisattava: Tuote):
        self._tavaroita += 1

    def poista_tuote(self, poistettava: Tuote):
        pass

    def tyhjenna(self):
        pass

    def ostokset(self):
        pass
