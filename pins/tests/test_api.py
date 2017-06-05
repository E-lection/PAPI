from django.test import TestCase
from django.urls import reverse
from mock import patch

from ..models import PinCode

STATION_PK = 1
ELIGIBLE_VOTER_PK = 1
INELIGBLE_VOTER_PK = 37

RESPONSE_OK = 200

class GetPinCodeTests(TestCase):

    def test_endpoint_returns_repsonse(self):
        url = reverse('pins:get_pin_code', args=(STATION_PK, ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_generate_pin_returns_none_for_invalid_voter(self):
        url = reverse('pins:get_pin_code', args=(STATION_PK, INELIGBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, { 'success' : False,
                                                 'pin_code' : None })

    @patch('pins.pin_code_generator.SystemRandom.randrange', return_value=123456)
    @patch('pins.pin_code_generator.get_and_check_votability', return_value=True)
    def test_generate_pin_returns_pin_for_eligible_voter(self, _1, _2):
        url = reverse('pins:get_pin_code', args=(STATION_PK, ELIGIBLE_VOTER_PK,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)
        self.assertJSONEqual(response.content, { 'success' : True,
                                                 'pin_code' : 123456 })

class VerifyPinCodeTests(TestCase):

    def test_endpoint_returns_repsonse(self):
        url = reverse('pins:verify_pin_code', args=(STATION_PK, 123456,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, RESPONSE_OK)

    def test_verify_valid_pin_for_eligible_voter(self):
        pass
