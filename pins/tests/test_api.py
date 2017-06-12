from django.test import TestCase
from django.urls import reverse
from mock import patch

from ..models import PinCode

STATION_PK = 1
ELIGIBLE_VOTER_PK = 1
INELIGBLE_VOTER_PK = 37

VALID_PIN = 123456
INVALID_PIN = 987654

RESPONSE_OK = 200


def create_pin(station_id, voter_id, pin_code):
    PinCode.objects.create(
        station=station_id, voter=voter_id, pin_code=pin_code)


class GetPinCodeTests(TestCase):

    @patch('pins.views.activate_pin', return_value=True)
    def test_endpoint_returns_repsonse(self, *_):
        url = reverse('pins:get_pin_code', args=(
            STATION_PK, ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    @patch('pins.views.activate_pin', return_value=True)
    def test_generate_pin_returns_none_for_invalid_voter(self, *_):
        url = reverse('pins:get_pin_code', args=(
            STATION_PK, INELIGBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'success': False,
                                                'pin_code': None})

    @patch('pins.pin_code_generator.SystemRandom.randrange', return_value=123456)
    @patch('pins.pin_code_generator.get_and_check_votability', return_value=True)
    @patch('pins.views.activate_pin', return_value=True)
    def test_generate_pin_returns_pin_for_eligible_voter(self, *_):
        url = reverse('pins:get_pin_code', args=(
            STATION_PK, ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'success': True,
                                                'pin_code': '123456'})


class VerifyPinCodeTests(TestCase):

    def test_endpoint_returns_repsonse(self):
        url = reverse('pins:verify_pin_code_and_check_eligibility', args=(STATION_PK, VALID_PIN,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_verify_pin_for_invalid_pin(self):
        url = reverse('pins:verify_pin_code_and_check_eligibility', args=(STATION_PK, INVALID_PIN,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'already_voted' : None,
                                                'valid_pin' : False})

    @patch('pins.views.get_and_check_votability', return_value=True)
    def test_verify_valid_pin_for_eligible_voter(self, *_):
        create_pin(station_id=STATION_PK,
                   voter_id=ELIGIBLE_VOTER_PK, pin_code=VALID_PIN)
        url = reverse('pins:verify_pin_code_and_check_eligibility', args=(STATION_PK, VALID_PIN,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'already_voted' : False,
                                                'valid_pin' : True})

    @patch('pins.views.get_and_check_votability', return_value=False)
    def test_verify_valid_pin_for_ineligible_voter(self, *_):
        create_pin(station_id=STATION_PK,
                   voter_id=ELIGIBLE_VOTER_PK, pin_code=VALID_PIN)
        url = reverse('pins:verify_pin_code_and_check_eligibility', args=(STATION_PK, VALID_PIN,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, {'already_voted' : True,
                                                'valid_pin' : True})
