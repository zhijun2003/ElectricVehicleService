from django.http import JsonResponse

from .models import ChargingRecord, RepairRecord


def get_statistics(request):
    if request.method == 'GET':
        charging_records = ChargingRecord.objects.count()
        repair_records = RepairRecord.objects.count()
        return JsonResponse(
            {'status': 'success', 'data': {'charging_records': charging_records, 'repair_records': repair_records}})


class ChargingStatisticsView(APIView):
    def get(self, request):
        # 增加时间段过滤
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = ChargingRecord.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(
                start_time__date__range=[start_date, end_date]
            )

        # 新增统计维度
        stats = queryset.aggregate(
            total_energy=Sum('energy_used'),
            avg_duration=Avg(F('end_time') - F('start_time')),
            peak_hour=Hour('start_time__hour')
        )

        # 按充电桩类型统计
        station_stats = ChargingStation.objects.values('power').annotate(
            total_usage=Sum('records__energy_used'),
            usage_count=Count('records')
        )

        return Response({
            'time_range_stats': stats,
            'station_type_stats': station_stats
        })
