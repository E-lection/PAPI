from django.http import HttpResponse, JsonResponse


def index(request):
    return HttpResponse("Hello, world. You're at the pins index.")

def get_pin_code(request, station_id, voter_id):
    return JsonResponse({ 'success' : False,
                          'pin_code' : None })
