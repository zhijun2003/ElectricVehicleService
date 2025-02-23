# charging/views.py
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChargingStation, ChargingRecord
from .permissions import IsStaffOrReadOnly
from .serializers import (
    ChargingStationSerializer,
    ChargingRecordSerializer,
    ReservationSerializer
)


class ChargingStationViewSet(viewsets.ModelViewSet):
    queryset = ChargingStation.objects.all()
    serializer_class = ChargingStationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    filterset_fields = ['status', 'power']
    search_fields = ['name', 'location']
    pagination_class = PageNumberPagination

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def reserve(self, request, pk=None):
        """预约充电桩"""
        station = self.get_object()
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            # 使用select_for_update防止并发问题
            station = ChargingStation.objects.select_for_update().get(pk=pk)

            if station.status not in ['available', 'reserved']:
                return Response(
                    {'detail': '当前状态不可预约'},
                    status=status.HTTP_409_CONFLICT
                )

            if station.reserved_by and station.reserved_by != request.user:
                return Response(
                    {'detail': '已被其他用户预约'},
                    status=status.HTTP_409_CONFLICT
                )

            station.status = 'reserved'
            station.reserved_by = request.user
            station.reservation_expiry = timezone.now() + timezone.timedelta(minutes=30)
            station.save()

            return Response({
                'reservation_id': station.id,
                'expiry_time': station.reservation_expiry
            }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def near_me(self, request):
        """附近充电桩查询"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 5)  # 默认5公里

        # 实现基于地理位置的查询逻辑
        queryset = ChargingStation.objects.filter(
            gps_lat__range=(float(lat) - 0.045, float(lat) + 0.045),  # 约5公里范围
            gps_lng__range=(float(lng) - 0.045, float(lng) + 0.045),
            status__in=['available', 'reserved']
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ChargingRecordViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ChargingRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChargingRecord.objects.filter(user=self.request.user)
