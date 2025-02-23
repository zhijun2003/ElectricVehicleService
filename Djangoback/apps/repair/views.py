# --------------- views.py ---------------
import json

from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination

from .models import RepairOrder


class RepairPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'

def submit_repair_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            required_fields = ['vehicle_model', 'license_plate', 'issue_description']
            if not all(field in data for field in required_fields):
                return JsonResponse({'status': 'error', 'message': '缺少必填字段'}, status=400)

            record = RepairOrder.objects.create(
                user=request.user,
                vehicle_model=data['vehicle_model'],
                license_plate=data['license_plate'],
                issue_description=data['issue_description'],
                image_url=data.get('image_url')
            )
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': record.id,
                    'license_plate': record.license_plate,
                    'status': record.status
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def get_repair_records(request):
    if request.method == 'GET':
        try:
            records = RepairOrder.objects.filter(user=request.user).order_by('-created_at')
            records_data = [{
                'id': record.id,
                'vehicle_model': record.vehicle_model,
                'license_plate': record.license_plate,
                'issue_description': record.issue_description,
                'status': record.status,
                'created_at': record.created_at.strftime('%Y-%m-%d %H:%M'),
                'image_url': record.image_url
            } for record in records]
            return JsonResponse({'status': 'success', 'data': records_data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def update_repair_record(request, record_id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            record = RepairOrder.objects.get(id=record_id, user=request.user)
            if 'status' in data:
                record.status = data['status']
                record.save()
            return JsonResponse({'status': 'success', 'data': {'new_status': record.status}})
        except RepairOrder.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': '工单不存在'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
