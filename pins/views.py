from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import PinCode
from .api_utils import get_and_check_votability, make_voter_ineligible
from .pin_code_generator import generate_pin_code


def index(request):
    return HttpResponse("Pins database is online.")


def get_pin_code(request, station_id, voter_id):
    pin_code = generate_pin_code(station_id=station_id, voter_id=voter_id)
    return JsonResponse({'success': pin_code != None,
                         'pin_code': str(pin_code) if pin_code else None})


def verify_pin_code_and_check_eligibility(request, station_id, pin_code):
    try:
        pin_object = PinCode.objects.get(station=station_id, pin_code=pin_code)
        # Pin exists #
        if get_and_check_votability(pin_object.voter):
            return JsonResponse({'valid_pin': True,
                                 'already_voted': False})
        return JsonResponse({'valid_pin': True,
                             'already_voted': True})
    except ObjectDoesNotExist:
        return JsonResponse({'valid_pin': False,
                             'already_voted': None})


def verify_pin_code_and_make_ineligible(request, station_id, pin_code):
    try:
        pin_object = PinCode.objects.get(station=station_id, pin_code=pin_code)
        # Pin exists #
        if make_voter_ineligible(pin_object.voter):
            PinCode.objects.get(station=station_id, pin_code=pin_code).delete()
            return JsonResponse({'success': True})
    except ObjectDoesNotExist:
        pass
    return JsonResponse({'success': True})
