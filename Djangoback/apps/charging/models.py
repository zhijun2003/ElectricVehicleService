# charging/models.py
from django.conf import settings
from django.db import models


class ChargingStation(models.Model):
    STATUS_CHOICES = [
        ('available', '空闲可用'),
        ('occupied', '使用中'),
        ('reserved', '已预约'),
        ('maintenance', '维护中')
    ]

    name = models.CharField(max_length=100, verbose_name='充电桩名称')
    location = models.CharField(max_length=200, verbose_name='详细地址')
    gps_lat = models.FloatField(verbose_name='纬度')
    gps_lng = models.FloatField(verbose_name='经度')
    power = models.PositiveIntegerField(verbose_name='功率(kW)', default=60)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='当前状态'
    )
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='费率(元/度)'
    )
    reserved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations',
        verbose_name='预约用户'
    )
    reservation_expiry = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='预约到期时间'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '充电桩'
        verbose_name_plural = '充电桩'
        indexes = [
            models.Index(fields=['gps_lat', 'gps_lng']),
            models.Index(fields=['status'])
        ]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"


class ChargingRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='charging_records',
        verbose_name='用户'
    )
    station = models.ForeignKey(
        ChargingStation,
        on_delete=models.CASCADE,
        related_name='records',
        verbose_name='充电桩'
    )
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    energy_used = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='用电量(度)'
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='费用金额'
    )

    class Meta:
        verbose_name = '充电记录'
        verbose_name_plural = '充电记录'
        ordering = ['-start_time']
