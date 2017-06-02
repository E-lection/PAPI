from django.core.exceptions import ObjectDoesNotExist
from random import SystemRandom

from .models import PinCode


"""
THINGS THAT THE PIN CODE GENERATOR NEEDS TO DO:
    CHECK A VOTER IS ELIGIBLE TO VOTE
    INVALIDATE A VOTERS PIN CODE IF ONE ALREADY EXISTS
    PIN CODES ARE UNIQUE TO A STATION
    GENERATE A UNIQUE RANDOM PIN CODE
"""

def generate_pin_code(voter_id, station_id):
    # Does the voter exist and can they vote?
    if get_and_check_votability(voter_id):
        try:
            # Invalidate existing pin code if one exists
            PinCode.objects.get(voter=voter_id).delete()
        except ObjectDoesNotExist:
            pass
        while True:
            # pin_code = random.randint(0,1000000)
            ran_gen = SystemRandom()
            pin_code = ran_gen.randrange(1000000)
            try:
                # Pin codes should be unique to a station
                PinCode.objects.get(pin_code=pin_code, station=station_id)
            except ObjectDoesNotExist:
                # If a pin code doesn't exist return it
                PinCode.objects.create(pin_code=pin_code, voter=voter_id, station=station_id)
                return pin_code
