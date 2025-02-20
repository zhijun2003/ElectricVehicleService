from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction, DatabaseError
from django.core.exceptions import PermissionDenied, ValidationError
import json
import logging
from .models import ChargingStation, ChargingRecord

logger = logging.getLogger(__name__)

def handle_json_request(view_func):
    """统一处理JSON请求的装饰器"""
    def wrapper(request, *args, **kwargs):
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Unsupported Content-Type'}, status=415)
            
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
            
        return view_func(request, data, *args, **kwargs)
    return wrapper

# 充电桩管理接口
@require_http_methods(["POST"])
@login_required
@handle_json_request
def add_charging_station(request, data):
    """创建充电桩（需要管理员权限）"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        with transaction.atomic():
            station = ChargingStation.objects.create(
                location=data['location'].strip(),
                status=data.get('status', 'available')
            )
            return JsonResponse({
                'id': station.id,
                'location': station.location,
                'status': station.status
            }, status=201)
    except KeyError as e:
        logger.warning(f"Missing required field: {e}")
        return JsonResponse({'error': f'Missing required field: {e}'}, status=400)
    except DatabaseError as e:
        logger.error(f"Database error in add_charging_station: {str(e)}")
        return JsonResponse({'error': 'Database operation failed'}, status=500)

@require_http_methods(["PUT"])
@login_required
@handle_json_request
def update_charging_station(request, data, station_id):
    """更新充电桩信息"""
    try:
        with transaction.atomic():
            station = ChargingStation.objects.select_for_update().get(id=station_id)
            
            # 字段更新校验
            if 'location' in data:
                station.location = data['location'].strip()
            if 'status' in data:
                if not station.is_valid_status(data['status']):
                    raise ValidationError('Invalid status value')
                station.status = data['status']
                
            station.full_clean()
            station.save()
            return JsonResponse({
                'id': station.id,
                'new_location': station.location,
                'new_status': station.status
            })
    except ChargingStation.DoesNotExist:
        return JsonResponse({'error': 'Station not found'}, status=404)
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

@require_http_methods(["DELETE"])
@login_required
def delete_charging_station(request, station_id):
    """删除充电桩"""
    try:
        if not request.user.is_staff:
            raise PermissionDenied
            
        station = ChargingStation.objects.get(id=station_id)
        station.delete()
        return JsonResponse({'message': 'Station deleted'}, status=204)
    except ChargingStation.DoesNotExist:
        return JsonResponse({'error': 'Station not found'}, status=404)
    except PermissionDenied:
        return JsonResponse({'error': 'Admin required'}, status=403)

# 充电桩查询接口
@require_http_methods(["GET"])
def get_charging_stations(request):
    """获取所有充电桩"""
    try:
        stations = ChargingStation.objects.values('id', 'location', 'status')
        return JsonResponse({'data': list(stations)})
    except DatabaseError as e:
        logger.error(f"Database error: {str(e)}")
        return JsonResponse({'error': 'Service unavailable'}, status=503)

# 充电桩预约接口
@require_http_methods(["POST"])
@login_required
@handle_json_request
def reserve_charging_station(request, data, station_id):
    """预约充电桩"""
    try:
        with transaction.atomic():
            station = ChargingStation.objects.select_for_update().get(id=station_id)
            
            if station.status != 'available':
                return JsonResponse({
                    'error': f'Station is {station.status}',
                    'current_state': station.status
                }, status=409)
                
            station.status = 'reserved'
            station.reserved_by = request.user
            station.save()
            
            return JsonResponse({
                'reservation_id': station.id,
                'expiration_time': station.reservation_expiry  # 需在模型中实现
            }, status=201)
    except ChargingStation.DoesNotExist:
        return JsonResponse({'error': 'Station not found'}, status=404)

# 充电记录查询
@require_http_methods(["GET"])
@login_required
def get_charging_records(request):
    """获取用户充电记录"""
    try:
        records = ChargingRecord.objects.filter(
            user=request.user
        ).select_related('station').values(
            'id',
            'station_id',
            'start_time',
            'end_time',
            'station__location'  # 关联查询
        )
        return JsonResponse({'data': list(records)})
    except DatabaseError as e:
        logger.error(f"Records query failed: {str(e)}")
        return JsonResponse({'error': 'Failed to retrieve records'}, status=500)