from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import ChargingStation

@csrf_exempt
def add_charging_station(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        location = data.get('location')
        status = data.get('status')
        charging_station = ChargingStation.objects.create(location=location, status=status)
        return JsonResponse({'status': 'success', 'message': 'Charging station added successfully'})

@csrf_exempt
def update_charging_station(request, station_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        charging_station = ChargingStation.objects.get(id=station_id)
        charging_station.location = data.get('location', charging_station.location)
        charging_station.status = data.get('status', charging_station.status)
        charging_station.save()
        return JsonResponse({'status': 'success', 'message': 'Charging station updated successfully'})

@csrf_exempt
def delete_charging_station(request, station_id):
    if request.method == 'DELETE':
        charging_station = ChargingStation.objects.get(id=station_id)
        charging_station.delete()
        return JsonResponse({'status': 'success', 'message': 'Charging station deleted successfully'})