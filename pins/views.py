from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .pin_code_generator import generate_pin_code

def index(request):
    return HttpResponse("Pins database is online.")

def get_pin_code(request, station_id, voter_id):
    pin_code = generate_pin_code(station_id=station_id, voter_id=voter_id)
    return JsonResponse({ 'success' : pin_code != None,
                          'pin_code' : pin_code })


def verify_pin_code(request, station_id, pin_code):
    # try:
    #     pin_object = PinCode.objects.get(station_id=station_id, pin_code=pin_code)
    # except ObjectDoesNotExist:
        # return
    return HttpResponse()
