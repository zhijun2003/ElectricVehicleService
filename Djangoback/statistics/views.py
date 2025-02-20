from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChargingRecord, RepairRecord

@csrf_exempt
def get_statistics(request):
    if request.method == 'GET':
        charging_records = ChargingRecord.objects.count()
        repair_records = RepairRecord.objects.count()
        return JsonResponse({'status': 'success', 'data': {'charging_records': charging_records, 'repair_records': repair_records}})