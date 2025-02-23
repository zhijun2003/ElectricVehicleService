from rest_framework import serializers

from .models import ChargingStation, ChargingRecord


class ChargingStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingStation
        fields = '__all__'
        read_only_fields = ['reserved_by', 'reservation_expiry']


class ReservationSerializer(serializers.Serializer):
    duration = serializers.IntegerField(
        min_value=15,
        max_value=120,
        help_text="预约时长（分钟）"
    )


class ChargingRecordSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='station.name', read_only=True)

    class Meta:
        model = ChargingRecord
        fields = '__all__'
