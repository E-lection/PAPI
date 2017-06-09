import urllib2
import json

VOTER_API_URL = 'http://voting.eelection.co.uk/check_votable/'


def check_votablity(votability_data):
    return votability_data['voter_exists'] and not votability_data['used_vote']


def get_votablity_data(voter_id):
    url = VOTER_API_URL + str(voter_id) + '/'
    response = urllib2.urlopen(url)
    return json.loads(response.read())


def get_and_check_votability(voter_id):
    return check_votablity(get_votablity_data(voter_id))
