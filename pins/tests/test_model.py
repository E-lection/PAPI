from django.test import TestCase

from ..models import PinCode

class PinCodeModelTests(TestCase):

    def test_string_representation(self):
        pin_code = PinCode(pincode=23, voter=1, station=1)

        self.assertEqual(str(pin_code), '000023')
