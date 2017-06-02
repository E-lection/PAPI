from django.test import TestCase

from ..pin_code_generator import generate_pin_code

class PinCodeGeneratorTests(TestCase):

    pass
    # def test_pin_code_generator_returns_unique_code(self):
    #     pin_codes = []
    #
    #     i = 0
    #     while i < 1:
    #         i = i + 1
    #         pin_code = generate_pin_code(voter_id=i, station_id=1)
    #         pin_codes.append(pin_code)
    #
    #     self.assertFalse(self.anydup(pin_codes))
    #
    # def anydup(self, thelist):
    #   seen = set()
    #   for x in thelist:
    #     if x in seen: return True
    #     seen.add(x)
    #   return False
