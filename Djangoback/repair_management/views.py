from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import RepairRecord

@csrf_exempt
def submit_repair_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        description = data.get('description')
        image_url = data.get('image_url')
        record = RepairRecord.objects.create(user=user, description=description, image_url=image_url)
        return JsonResponse({'status': 'success', 'message': 'Repair record submitted successfully'})

@csrf_exempt
def get_repair_records(request):
    if request.method == 'GET':
        user = request.user
        records = RepairRecord.objects.filter(user=user)
        records_data = [{'id': record.id, 'description': record.description, 'status': record.status} for record in records]
        return JsonResponse({'status': 'success', 'data': records_data})

@csrf_exempt
def update_repair_record(request, record_id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        record = RepairRecord.objects.get(id=record_id)
        record.status = data.get('status', record.status)
        record.save()
        return JsonResponse({'status': 'success', 'message': 'Repair record updated successfully'})
