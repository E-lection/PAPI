import datetime

from django.test import TestCase
from django.utils import timezone

from ..models import PinCode

class PinCodeModelTests(TestCase):

    def test_string_representation(self):
        pin_code = PinCode(pin_code=23, voter=1, station=1)

        self.assertEqual(str(pin_code), '000023')

    def test_pin_valid_when_made(self):
        PinCode(pin_code=23, voter=1, station=1).save()

        self.assertTrue(PinCode.objects.get(pin_code=23).is_valid())

    def test_pin_invalid_after_an_hour(self):
        hour_ago = timezone.now() - datetime.timedelta(minutes=60)
        pin_code = PinCode(pin_code=23, voter=1, station=1, creation=hour_ago)

        self.assertFalse(pin_code.is_valid())
