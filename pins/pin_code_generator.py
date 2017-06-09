from django.core.exceptions import ObjectDoesNotExist
from random import SystemRandom

from .models import PinCode
from .api_utils import get_and_check_votability

VOTERS_GENERATING_PINS = []


def generate_pin_code(station_id, voter_id):
    # Does the voter exist and can they vote?
    if get_and_check_votability(voter_id):
        voter_enter_pin_generation(voter_id)
        pin_object = None
        try:
            # Check for existing pin code if one exists
            pin_object = PinCode.objects.get(voter=voter_id)
        except ObjectDoesNotExist:
            pin_object = PinCode(voter=voter_id, station=station_id, pin_code=0)
            pin_object.save()
        while True:
            ran_gen = SystemRandom()
            pin_code = ran_gen.randrange(1000000)
            try:
                # Pin codes should be unique to a station
                PinCode.objects.get(pin_code=pin_code, station=station_id)
            except ObjectDoesNotExist:
                # If a pin code doesn't exist return it
                pin_object.pin_code = pin_code
                pin_object.save()
                voter_leave_pin_generation(voter_id)
                return pin_code
        voter_leave_pin_generation(voter_id)


def voter_enter_pin_generation(voter_id):
    while voter_id in VOTERS_GENERATING_PINS:
        pass
    else:
        VOTERS_GENERATING_PINS.append(voter_id)


def voter_leave_pin_generation(voter_id):
    VOTERS_GENERATING_PINS.remove(voter_id)
