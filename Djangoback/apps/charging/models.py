# charging_records/models.py
from django.db import models
from django.contrib.auth.models import User

class ChargingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey('charging_stations.ChargingStation', on_delete=models.CASCADE)
    # 其他字段...
