from django.http import HttpResponse, JsonResponse

from .pin_code_generator import generate_pin_code

def index(request):
    return HttpResponse("Pins database is online.")

def get_pin_code(request, station_id, voter_id):
    pin_code = generate_pin_code(voter_id=voter_id, station_id=station_id)
    return JsonResponse({ 'success' : pin_code != None,
                          'pin_code' : pin_code })
