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

@csrf_exempt
def get_charging_stations(request):
    if request.method == 'GET':
        stations = ChargingStation.objects.all()
        stations_data = [{'id': station.id, 'location': station.location, 'status': station.status} for station in stations]
        return JsonResponse({'status': 'success', 'data': stations_data})

@csrf_exempt
def reserve_charging_station(request, station_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        station = ChargingStation.objects.get(id=station_id)
        if station.status == 'available':
            station.status = 'reserved'
            station.reserved_by = user
            station.save()
            return JsonResponse({'status': 'success', 'message': 'Charging station reserved successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Charging station is not available'})

@csrf_exempt
def get_charging_records(request):
    if request.method == 'GET':
        user = request.user
        records = ChargingRecord.objects.filter(user=user)
        records_data = [{'id': record.id, 'station_id': record.station.id, 'start_time': record.start_time, 'end_time': record.end_time} for record in records]
        return JsonResponse({'status': 'success', 'data': records_data})
