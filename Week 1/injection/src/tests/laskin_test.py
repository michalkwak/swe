import unittest
from laskin import Laskin  # "Laskin" = Calculator


# Stub replacement for KonsoliIO (console IO) so tests can feed input
# and capture output without touching the real terminal.
class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs  # values returned one by one when the calculator reads input
        self.outputs = []  # everything the calculator writes is collected here

    # "lue" = read: return the next queued input instead of calling input()
    def lue(self, teksti):
        return self.inputs.pop(0)

    # "kirjoita" = write: store the output instead of printing it
    def kirjoita(self, teksti):
        self.outputs.append(teksti)


class TestLaskin(unittest.TestCase):
    # "yksi summa oikein" = one sum correct
    def test_yksi_summa_oikein(self):
        # Inputs: 1 + 3, then -9999 to stop the calculator
        io = StubIO(["1", "3", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()  # "suorita" = run

        self.assertEqual(io.outputs[0], "Summa: 4")  # "Summa" = Sum

    # "kaksi summaa oikein" = two sums correct
    def test_kaksi_summaa_oikein(self):
        # Inputs: first calculation 1 + 3, second calculation 5 + 7,
        # then -9999 to stop the calculator
        io = StubIO(["1", "3", "5", "7", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()

        # Each calculation should produce its own correct result, in order
        self.assertEqual(io.outputs[0], "Summa: 4")
        self.assertEqual(io.outputs[1], "Summa: 12")
        # Exactly two results should have been written
        self.assertEqual(len(io.outputs), 2)
