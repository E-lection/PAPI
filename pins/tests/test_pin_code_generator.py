from django.test import TestCase
from mock import patch

from ..models import PinCode
from ..pin_code_generator import generate_pin_code

STATION_ID = 1
ELIGIBLE_VOTER_ID = 1
ELIGIBLE_VOTER_ID_2 = 2
INELIGIBLE_VOTER_ID = 74

PIN_CODES = [567890, 567890, 123456]
i = 0

def pin_code_sequence(range):
    global i
    pin_code = PIN_CODES[i]
    i += 1
    return pin_code

def create_pin(station_id, voter_id, pin_code):
    PinCode.objects.create(station=station_id, voter=voter_id, pin_code=pin_code)

class PinCodeGeneratorTests(TestCase):

    @patch('pins.pin_code_generator.get_and_check_votability', return_value=False)
    def test_ineligible_voter_pin_generation_returns_none(self, *_):
        self.assertEqual(generate_pin_code(STATION_ID, INELIGIBLE_VOTER_ID), None)

    @patch('pins.pin_code_generator.SystemRandom.randrange', return_value=123456)
    @patch('pins.pin_code_generator.get_and_check_votability', return_value=True)
    def test_eligble_voter_pin_generation_returns_pin(self, *_):
        self.assertEqual(generate_pin_code(STATION_ID, ELIGIBLE_VOTER_ID), 123456)

    @patch('pins.pin_code_generator.SystemRandom.randrange', return_value=123456)
    @patch('pins.pin_code_generator.get_and_check_votability', return_value=True)
    def test_existing_pin_for_eligible_voter_is_replaced(self, *_):
        create_pin(station_id=STATION_ID, voter_id=ELIGIBLE_VOTER_ID, pin_code=567890)
        self.assertEqual(generate_pin_code(STATION_ID, ELIGIBLE_VOTER_ID), 123456)
        pin_object = PinCode.objects.get(station=STATION_ID, voter=ELIGIBLE_VOTER_ID)
        self.assertEqual(pin_object.pin_code, 123456)

    #Generate the same pin code on first call to randrange as already exists
    @patch('pins.pin_code_generator.SystemRandom.randrange', side_effect=pin_code_sequence)
    @patch('pins.pin_code_generator.get_and_check_votability', return_value=True)
    def test_pins_are_unique_to_station(self, *_):
        create_pin(station_id=STATION_ID, voter_id=ELIGIBLE_VOTER_ID, pin_code=PIN_CODES[0])
        self.assertEqual(generate_pin_code(STATION_ID, ELIGIBLE_VOTER_ID_2), PIN_CODES[2])
