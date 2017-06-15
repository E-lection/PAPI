import urllib2
import urllib
import json

from api_key_verification import PINS_KEY

VOTER_API_URL = 'http://voting.eelection.co.uk/check_votable/'
PIN_ACTIVATION_URL = 'http://voting.eelection.co.uk/set_voter_has_active_pin/'
VOTER_INELIGIBLE_URL = 'http://voting.eelection.co.uk/make_voter_ineligible/'

def check_votablity(votability_data):
    # Returns TRUE if someone can vote
    return votability_data['voter_exists'] and not votability_data['used_vote']


def get_votablity_data(voter_id):
    url = VOTER_API_URL + urllib.quote(str(voter_id)) + '/'
    request = urllib2.Request(url)
    request.add_header("Authorization", PINS_KEY);
    response = urllib2.urlopen(request)
    return json.loads(response.read())


def get_and_check_votability(voter_id):
    # Returns TRUE if someone can vote
    return check_votablity(get_votablity_data(voter_id))


def make_voter_ineligible(voter_id):
    url = VOTER_INELIGIBLE_URL + urllib.quote(str(voter_id)) + '/'
    request = urllib2.Request(url)
    request.add_header("Authorization", PINS_KEY);
    response = urllib2.urlopen(request)
    return json.loads(response.read())['success']


def activate_pin(voter_id):
    url = PIN_ACTIVATION_URL + urllib.quote(str(voter_id)) + '/'
    request = urllib2.Request(url)
    request.add_header("Authorization", PINS_KEY);
    response = urllib2.urlopen(request)
    return json.loads(response.read())
