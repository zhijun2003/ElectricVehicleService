from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from models import ChargingRecord


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_charging_records(request):
    try:
        # 直接获取当前用户所有充电记录
        queryset = ChargingRecord.objects.filter(user=request.user)

        # 直接序列化全部数据
        serializer = ChargingRecordSerializer(queryset, many=True)
        return Response({'results': serializer.data})

    except Exception as e:
        logger.error(f'充电记录查询失败: {str(e)}')
        return Response({'error': '服务器错误'}, status=500)
